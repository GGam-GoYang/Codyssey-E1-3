from user_manual import run_user
from json_manual import run_json


def select_mode():
    while True:
        print("메뉴 선택")
        print("1 : 사용자 입력")
        print("2 : JSON 모드")

        if (inp := int(input("입력 : "))) not in [1, 2]:
            print("1 또는 2를 선택하셔야 합니다!")
            continue
        return inp
        

def main():
    inp = select_mode()
    if inp == 1:
        run_user()
    elif inp == 2:
        run_json()

if __name__ == "__main__":
    main()