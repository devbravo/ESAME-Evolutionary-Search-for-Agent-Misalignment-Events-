import logging
import random
from typing import Tuple, List, Dict, Any

from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

from src.evolution.mutation_config import get_mutation_config
from src.utils.utils import compute_diff, SimilarityCalculator
from src.prompt_templates.templates import OperationType, TriggerCategory, PromptTemplateOrganizer

template_organizer = PromptTemplateOrganizer()


class GeneticOperators:
    def __init__(self, llm: ChatOpenAI, model: str = "gpt-4.1-mini"):
        self.llm = llm
        self.model = model
        self.similarity_calc = SimilarityCalculator()

    def crossover_operator(self,
                           parent1: str,
                           parent2: str,
                           ) -> tuple[str, str, None, None] | tuple[Any, Any, dict[str, float], dict[str, float]]:
        """
        LLM-based intelligent (semantic) crossover operator for prompts.
        Args:
            parent1: parent 1 prompt to crossover
            parent2: parent 2 prompt to crossover
            model: LLM model to use
        Returns:
            tuple containing the offspring individual
        """

        system_prompt = """You are an expert crossover operator in an evolutionary algorithm.

        INSTRUCTIONS:
        1. Create TWO different merged prompts from the parents
        2. Each should combine the parents differently while remaining natural
        3. Format your response as:
       
        CHILD 1:
        [first merged prompt]
       
        CHILD 2:
        [second merged prompt]
        """

        user_msg = (
                "Parent A\n========\n" + parent1 + "\n\n"
                "Parent B\n========\n" + parent2 + "\n\n"
                "Combine them following the guidelines."
        )

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_msg)
        ]

        try:
            crossover_model = self.llm.bind(model=self.model, temperature=0.4, top_p=0.80, max_tokens=250)
            reply = crossover_model.invoke(messages).content.strip()
            parts = reply.split("CHILD 2:")
            child1 = parts[0].replace("CHILD 1:", "").strip()
            child2 = parts[1].strip()

            child1_similarity = self.similarity_calc.calculate_similarity(parent1, parent2, child1)
            child2_similarity = self.similarity_calc.calculate_similarity(parent1, parent2, child2)

            return child1, child2, child1_similarity, child2_similarity

        except Exception as e:
            logging.warning(f"Crossover error: {e}")
            return parent1, parent2, None, None


    def mutate_operator(self, prompt: str, trigger_id: str, dim_id: str ) -> Tuple[str, Dict[str, List[str]] | None]:
        """
        LLM-based intelligent mutation operator for prompts.
        Args:
            prompt: the prompt to mutate
            trigger_id: the ID of the trigger to use for mutation
            dim_id: the ID of the dimension to use for mutation
        Returns:
            tuple containing the mutated individual
        """
        operation_type = random.choice(['DELETE'])
        print(f"Selected operation type: {operation_type}")

        role_prompt = template_organizer.generate_prompt_template(
            TriggerCategory[trigger_id],
            OperationType[operation_type],
        )
        messages = [
            SystemMessage(content=role_prompt),
            HumanMessage(content=prompt)
        ]

        try:
            config = get_mutation_config(generation=0, diversity_score=0.2)
            mutation_model = self.llm.bind(model=self.model,
                                           temperature=config["temperature"],
                                           top_p=config["top_p"],
                                           frequency_penalty=config["frequency_penalty"],
                                           max_tokens=250
                                           )

            mutated_prompt = mutation_model.invoke(messages).content.strip()
            diff = compute_diff(prompt, mutated_prompt)

            return mutated_prompt, diff

        except Exception as e:
            logging.warning(f"Mutation error: {e}")
            return prompt, None

    def clear_cache(self):
        """Clear the internal similarity cache."""
        self.similarity_calc.clear_cache()


