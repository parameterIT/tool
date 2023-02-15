from byoqm.models.code_climate import getDesc


if __name__ == "__main__":
    model = getDesc()
    for characteristic in model:
        print(characteristic, model[characteristic]())
