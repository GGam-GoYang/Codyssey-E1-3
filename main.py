from user_manual import run_user
from json_manual import run_json


def select_mode():
    """파라미터 없음. 메뉴를 반복 입력받는다. 반환: 정수 1 또는 2."""
    while True:
        print("메뉴 선택")
        print("1 : 사용자 입력")
        print("2 : JSON 모드")
        try:
            if (inp := int(input("입력 : "))) not in [1, 2]:
                print("1 또는 2를 선택하셔야 합니다!")
                continue
        except ValueError:
            print("정수만 입력 가능합니다!")
            continue
        
        return inp
        

def main():
    """파라미터 없음. 선택한 모드를 실행한다. 반환: None."""
    inp = select_mode()
    if inp == 1:
        run_user()
    elif inp == 2:
        run_json()

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n입력이 종료되었습니다.")
    except ValueError as error:
        print("계산 오류:", error)