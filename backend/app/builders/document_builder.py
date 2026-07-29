from app.models.pet import Pet


class DocumentBuilder:

    @staticmethod
    def build_pet(pet: Pet) -> str:
        return f"""
            Name: {pet.name}

            Species: {pet.species}

            Breed: {pet.breed}

            Gender: {pet.gender}

            Age: {pet.age}

            Description:
            {pet.description}
        """.strip()