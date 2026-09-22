from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class EvidenceRetriever:

    def __init__(self, segments):

        self.segments = segments

        # Local embedding model
        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        # Create embeddings for every expert response
        texts = [
            segment["text"]
            for segment in segments
        ]

        self.embeddings = self.model.encode(
            texts,
            convert_to_numpy=True
        )


    # ========================================================
    # STANDARD SEARCH
    # Used for Interview Guide and normal semantic retrieval
    # ========================================================

    def search(
        self,
        query,
        top_k=5,
        question_number=None
    ):

        # ----------------------------------------------------
        # 1. Select candidate evidence
        # ----------------------------------------------------

        candidate_indices = list(
            range(len(self.segments))
        )

        # For predefined interview questions,
        # restrict retrieval to that question.
        if question_number is not None:

            candidate_indices = [
                i
                for i, segment in enumerate(self.segments)
                if segment.get("question_number")
                == question_number
            ]


        # ----------------------------------------------------
        # 2. Convert query into embedding
        # ----------------------------------------------------

        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True
        )


        # ----------------------------------------------------
        # 3. Compare query against candidate evidence
        # ----------------------------------------------------

        candidate_embeddings = self.embeddings[
            candidate_indices
        ]

        similarities = cosine_similarity(
            query_embedding,
            candidate_embeddings
        )[0]


        # ----------------------------------------------------
        # 4. Rank by semantic similarity
        # ----------------------------------------------------

        ranked_positions = similarities.argsort()[::-1]


        # ----------------------------------------------------
        # 5. Build results
        # ----------------------------------------------------

        results = []

        for position in ranked_positions[:top_k]:

            original_index = candidate_indices[
                position
            ]

            result = self.segments[
                original_index
            ].copy()

            result["score"] = float(
                similarities[position]
            )

            results.append(result)


        return results


    # ========================================================
    # DIVERSE SEARCH
    # Used for Cross-Call Analysis
    # Ensures every market is represented.
    # ========================================================

    def search_diverse(
        self,
        query,
        per_country=3
    ):

        # ----------------------------------------------------
        # 1. Convert query into embedding
        # ----------------------------------------------------

        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True
        )


        # ----------------------------------------------------
        # 2. Calculate similarity against all evidence
        # ----------------------------------------------------

        similarities = cosine_similarity(
            query_embedding,
            self.embeddings
        )[0]


        # ----------------------------------------------------
        # 3. Find all countries
        # ----------------------------------------------------

        countries = sorted(
            set(
                segment["country"]
                for segment in self.segments
            )
        )


        results = []


        # ----------------------------------------------------
        # 4. Retrieve top evidence from EACH country
        # ----------------------------------------------------

        for country in countries:

            country_indices = [
                i
                for i, segment
                in enumerate(self.segments)
                if segment["country"] == country
            ]


            # Rank evidence within this country
            ranked_indices = sorted(
                country_indices,
                key=lambda i: similarities[i],
                reverse=True
            )


            # Take top N from this country
            for index in ranked_indices[
                :per_country
            ]:

                result = self.segments[
                    index
                ].copy()

                result["score"] = float(
                    similarities[index]
                )

                results.append(result)


        # ----------------------------------------------------
        # 5. Sort final results by relevance
        # ----------------------------------------------------

        results.sort(
            key=lambda item: item["score"],
            reverse=True
        )


        return results