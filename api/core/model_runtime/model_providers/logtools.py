import json


def log2file(class_name, obj):
    file_path = "./tmp.log"
    with open(file_path, "a") as f:
        f.write(class_name+"\n")
        json.dump(obj, f, ensure_ascii=False)
        f.write("\n")
        f.flush()


if __name__ == '__main__':
    log2file(__file__, {"aa":123})
    log2file(__file__,[{"bb": 456}])
