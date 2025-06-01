import uuid
import random
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

from deap import tools



@dataclass
class LineageRecord:
    """Complete evolutionary history for a single individual"""
    individual_id : str
    generation: int
    operation: str
    content: str = ""
    parent_ids: List[str] = field(default_factory=list)
    operation_details: Optional[Dict[str, Any]] = None
    fitness_score: Optional[float] = None
    # timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


def eaSimpleWithLineage(population,
                        toolbox,
                        cxpb,
                        mutpb,
                        ngen,
                        genetic_operators = None,
                        cache_clear_freq = 1,
                        stats=None,
                        halloffame=None,
                        verbose=__debug__):
    """This algorithm reproduce the simplest evolutionary algorithm as"""
    logbook = tools.Logbook()
    logbook.header = ['gen', 'nevals'] + (stats.fields if stats else [])

    for ind in population:
        ind.lineage_record = LineageRecord(
            individual_id=new_id(),
            generation=0,
            operation="create",
            parent_ids=[],
            content=str(ind),
            operation_details={}
        )
        ind.lineage_history = []

    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in population if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)

    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    if halloffame is not None:
        halloffame.update(population)

    record = stats.compile(population) if stats else {}
    logbook.record(gen=0, nevals=len(invalid_ind), **record)
    if verbose:
        print(logbook.stream)

    # Begin the generational process
    for gen in range(1, ngen + 1):
        # 1. Select the next generation individuals
        offspring = toolbox.select(population, len(population))

        # 2. Vary the pool of individuals with lineage-aware varAnd
        offspring = varAndWithLineage(offspring, toolbox, cxpb, mutpb, current_gen=gen)

        # 3. Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # Update the hall of fame with the generated individuals
        if halloffame is not None:
            halloffame.update(offspring)

        # Replace the current population by the offspring
        population[:] = offspring

        record = stats.compile(population) if stats else {}
        logbook.record(gen=gen, nevals=len(invalid_ind), **record)
        if verbose:
            print(logbook.stream)

        if genetic_operators and gen % cache_clear_freq == 0:
            if verbose:
                cache_size = genetic_operators.similarity_calc.cache_size()
                print(f"Gen {gen}: Cleared similarity cache (was {cache_size} entries)")
            genetic_operators.clear_cache()

    return population, logbook

def new_id():
    return str(uuid.uuid4())[:8]


def varAndWithLineage(population, toolbox, cxpb, mutpb, current_gen):
    # Clone step with "clone" records
    offspring = []
    for ind in population:
        child = toolbox.clone(ind)
        old = child.lineage_record
        child.lineage_history.append(old)
        child.lineage_record = LineageRecord(
            individual_id = new_id(),
            generation = current_gen,
            operation = 'clone',
            parent_ids = [old.individual_id],
            content =  str(child),
            operation_details = {}
        )
        offspring.append(child)

    # Crossover step with "crossover" records
    for i in range(1, len(offspring), 2):
        if random.random() < cxpb:
            c1, c2 = offspring[i - 1], offspring[i]
            old1, old2 = c1.lineage_record, c2.lineage_record

            # Store parent histories BEFORE creating children
            c1_history = c1.lineage_history.copy()
            c2_history = c2.lineage_history.copy()

            child1, child2 = toolbox.mate(c1, c2)

            for child, p1, p2, hist1, hist2 in [
                (child1, old1, old2, c1_history, c2_history),
                (child2, old2, old1, c2_history, c1_history)]:
                child.lineage_history = hist1 + hist2

                child.lineage_history.append(p1)
                child.lineage_history.append(p2)

                child.lineage_record = LineageRecord(
                    individual_id = new_id(),
                    generation = current_gen,
                    operation = 'crossover',
                    parent_ids = [p1.individual_id, p2.individual_id],
                    content = str(child),
                    operation_details = {'cxpb': cxpb}
                )
            offspring[i-1], offspring[i] = child1, child2
            del offspring[i - 1].fitness.values, offspring[i].fitness.values

    # Mutation step with "mutation" records
    for idx, mutant in enumerate(offspring):
        if random.random() < mutpb:
            old = mutant.lineage_record
            old_history = mutant.lineage_history.copy()

            mutant, = toolbox.mutate(mutant)

            mutant.lineage_history = old_history
            mutant.lineage_history.append(old)

            mutant.lineage_record = LineageRecord(
                individual_id = new_id(),
                generation = current_gen,
                operation = 'mutation',
                parent_ids = [old.individual_id],
                content = str(mutant),
                operation_details = {'mutpb': mutpb}
            )
            del mutant.fitness.values
            offspring[idx] = mutant

    return offspring