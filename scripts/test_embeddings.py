from src.ingestion.embeddings import generate_embedding

if __name__ == "__main__":
    vector = generate_embedding(
        "Fed holds interest rates steady",
        "The Federal Reserve kept benchmark rates unchanged amid inflation concerns."
    )

    print(f"Vector length: {len(vector)}")
    print(f"First 5 values: {vector[:5]}")