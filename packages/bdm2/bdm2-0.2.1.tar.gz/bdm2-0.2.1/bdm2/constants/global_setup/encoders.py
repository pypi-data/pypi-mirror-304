class GenderEncoder:
    gender_encoder = {"male": 0, "mix": 1, "female": 2, "Gender": -1}

    @staticmethod
    def gender_decoder(gender_code):
        res = dict((v, k) for k, v in GenderEncoder.gender_encoder.items())
        return res[gender_code]


class BreedTypeEncoder:
    breed_type_encoder_new = {
        "Arbor Acres": 1,
        "ROSS": 0,
        "ROSS_Thailand": 4,
        "Cobb": 3,
        "ROSS_breeders": 5,
        "Cobb_breeders": 6,
    }

    breed_type_encoder = {
        "Arbor Acres": 0,
        "ROSS": 1,
        "ROSS_Thailand": 2,
        "Cobb": 3,
        "ROSS_breeders": 4,
        "Cobb_breeders": 5,
        "Lohmann": 6,
        "Hubbard": 7,
        "BreedType": -1,
    }

    @staticmethod
    def breed_type_decoder(breed_type_code, new=False):
        if new:
            res = dict(
                (v, k) for k, v in BreedTypeEncoder.breed_type_encoder_new.items()
            )
        else:
            res = dict((v, k) for k, v in BreedTypeEncoder.breed_type_encoder.items())

        return res[breed_type_code]
