## Problem Statement

    The current flashcard generation pipeline is hardcoded for Mandarin. The core engineering team is currently occupied with other technical challenges, creating a bottleneck for Quality Assurance (QA). Because the system only supports Mandarin, the pool of potential external testers is severely limited. We need more people to run the generated .apkg files and identify edge cases in the 5-card multidirectional logic and audio isolation, but the language barrier prevents them from meaningfully evaluating the tool's effectiveness and visual outputs.

## Solution

    Expand the pipeline's architecture to support multiple languages, starting with English. By decoupling the language-specific logic (TTS voices, LLM prompts, Anki HTML/CSS templates, and data schemas) from the core orchestrator, the system will be able to generate English flashcard decks. This immediately broadens the available QA tester pool, allowing non-Mandarin speakers to validate the core architecture without needing to understand the underlying language data.

## User Stories

    1. As a core developer, I want a base data schema that can be extended for different languages, so that I don't have to duplicate the core validation logic for English.

    2. As a core developer, I want an English-specific data schema that includes an International Phonetic Alphabet (IPA) field, so that English pronunciation is correctly represented without relying on Mandarin Pinyin.

    3. As a core developer, I want a centralized configuration mapping for text-to-speech voices, so that I can dynamically assign an English voice model (e.g., "en-US-AriaNeural") instead of defaulting to the Mandarin model.

    4. As a core developer, I want the system prompt to dynamically accept the target and native languages via variables, so that the LLM generates accurate visual search terms regardless of the language being learned.

    5. As a project maintainer, I want to run the pipeline with a specific language parameter in the orchestrator, so that I can generate English decks locally and distribute them to the QA team.

    6. As a project maintainer, I want the semantic mapping rules in the LLM prompt to remain universal, so that abstract English concepts still generate concrete visual search terms for the image API (e.g., "although" -> "balance scale").

    7. As a QA tester, I want to receive an English .apkg file, so that I can evaluate the visual hierarchy, layout, and learning flow without needing to understand Mandarin.

    8. As a QA tester, I want the English flashcards to use language-specific HTML/CSS templates, so that the layout is visually balanced and doesn't contain awkward, empty spacing where Pinyin was originally intended to be.

    9. As a QA tester, I want the generated English audio to be separated into distinct word and sentence files, so that I can verify the audio isolation logic works correctly across different TTS voice models.

    10. As a language learner, I want the 5 multidirectional card types (Reading, Listening, Visual, Reverse, Context) to adapt seamlessly to English, so that my learning experience strictly follows the Minimum Information Principle.

## Implementation Decisions

    **Data Layer Polymorphism:** We will introduce a base data schema defining universal fields (target word, translation, semantic image search term, example sentence, sentence translation). We will implement strict subclasses for specific languages.
    Python

    ```python
    # Prototype Schema Decision
    class BaseFlashcard(BaseModel):
        target_word: str
        translation: str
        image_search_term_en: str
        example_sentence: str
        sentence_translation: str

    class EnglishFlashcard(BaseFlashcard):
        ipa_pronunciation: str

    class MandarinFlashcard(BaseFlashcard):
        pinyin: str
        hanzi: str
    ```


    **Audio Model Routing:** The orchestrator module will contain a language-to-voice configuration dictionary. The selected voice model string will be passed down to the audio generator module as a parameter, replacing the hardcoded Microsoft Xiaoxiao dependency.

    **Dynamic LLM Prompts:** The static system prompt in the LLM agent module will transition to an f-string template. It will inject {target_language} and {native_language} variables while explicitly retaining the universal rules for semantic proxy generation.

    **Anki Template Factory Pattern:** The Anki packaging module will utilize a factory pattern. It will map language codes to distinct HTML/CSS string constants and Anki model configurations, ensuring the specific fields from the data subclasses map correctly to the visual layouts.

    **Centralized Execution:** The pipeline execution and language selection will be managed directly in the orchestrator by the maintainer; testers will only interact with the final .apkg output.

## Testing Decisions

    **What makes a good test:** Tests should evaluate the structural integrity of the final output (the .apkg file) and the behavioral correctness of the LLM/TTS integration, rather than the internal processing steps. A successful test confirms that the final user sees the correct layout, hears the correct voice, and sees a semantically relevant image.

    **Modules to be tested:** * Data Validation (verifying the correct subclass rejects malformed language data).

        Audio Generation (verifying the TTS engine successfully switches voices and generates two distinct MP3s).

        Anki Packaging (verifying the HTML/CSS factory applies the correct template based on the language flag).

    **Prior Art:** The QA plan will utilize the existing 10 stress test scenarios (Cenários de Estresse) originally documented for Mandarin. These scenarios will be adapted to English to verify edge cases, API limits, and the success rate of the semantic image mapping.

## Out of Scope

    - A Command Line Interface (CLI) or external configuration files for end-users to run the script themselves.

    - A graphical user interface (GUI), web UI, or automation bot integration (e.g., n8n).

    - Creating highly customized, separate LLM prompts to handle extreme edge cases of English grammar (the universal template will suffice for this iteration).

    - Adding support for any languages other than English during this specific sprint.

## Further Notes

    This architectural pivot transitions the tool from a hardcoded personal utility into a scalable educational platform. By establishing polymorphism in the data and template layers now, adding a third or fourth language in the future will require minimal code changes.