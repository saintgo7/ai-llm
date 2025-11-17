"""
08. Chatbot - 간단한 규칙 기반 챗봇
"""
import re
import random
from datetime import datetime

class SimpleChatbot:
    def __init__(self, name="ChatBot"):
        self.name = name
        self.conversation_history = []
        self.user_name = None

        # 응답 패턴 정의
        self.patterns = {
            r'안녕|하이|헬로|hello|hi': [
                "안녕하세요! 무엇을 도와드릴까요?",
                f"안녕하세요! 저는 {self.name}입니다. 반갑습니다!",
                "안녕하세요! 오늘 기분이 어떠신가요?"
            ],
            r'이름|누구': [
                f"제 이름은 {self.name}입니다!",
                f"저는 {self.name}이라고 합니다. 당신의 이름은 무엇인가요?"
            ],
            r'날씨|weather': [
                "죄송하지만 날씨 정보는 제공하지 못합니다. 날씨 앱을 확인해보세요!",
                "오늘 날씨가 궁금하시군요. 창밖을 보시는 것은 어떨까요? 😊"
            ],
            r'시간|time|몇 시': [
                f"현재 시간은 {datetime.now().strftime('%H:%M:%S')}입니다.",
                f"지금은 {datetime.now().strftime('%Y년 %m월 %d일 %H시 %M분')}입니다."
            ],
            r'고마워|감사|thanks|thank': [
                "천만에요! 도움이 되어 기쁩니다.",
                "별말씀을요! 언제든 물어보세요.",
                "감사합니다! 더 필요한 것이 있나요?"
            ],
            r'잘가|bye|goodbye|나중에': [
                "안녕히 가세요! 좋은 하루 보내세요!",
                "다음에 또 만나요! 👋",
                "goodbye! 언제든 다시 찾아주세요!"
            ],
            r'기분|how are you|어때': [
                "저는 항상 좋습니다! 당신은 어떠신가요?",
                "잘 지내고 있습니다. 감사합니다!",
                "오늘 정말 좋은 날이네요!"
            ],
            r'도움|help|뭐 할': [
                "저는 간단한 대화를 나눌 수 있습니다. 날씨, 시간, 인사 등에 대해 물어보세요!",
                "무엇이든 물어보세요! 최선을 다해 답변하겠습니다.",
                "궁금한 것이 있으면 편하게 물어보세요!"
            ],
            r'농담|joke|재미있': [
                "프로그래머가 바에 간다. 맥주 1개를 주문한다... 아니 2개... 아니 0개... 아니 999999개...",
                "Q: 프로그래머의 자녀는 몇 명? A: 0명부터 시작!",
                "컴퓨터가 춤을 추면? 디스코! 😄"
            ]
        }

        # 기본 응답
        self.default_responses = [
            "흥미롭네요! 더 자세히 말씀해 주시겠어요?",
            "그것에 대해 더 알려주세요.",
            "이해했습니다. 계속 말씀해 주세요.",
            "음... 그 부분은 잘 모르겠어요. 다른 것을 물어보시겠어요?",
            "제가 아직 배우는 중입니다. 다른 질문을 해보시겠어요?"
        ]

    def get_response(self, user_input):
        """사용자 입력에 대한 응답 생성"""
        user_input = user_input.strip()

        if not user_input:
            return "무언가 말씀해 주세요!"

        # 대화 기록 저장
        self.conversation_history.append({
            'timestamp': datetime.now(),
            'user': user_input,
            'bot': None
        })

        # 패턴 매칭
        for pattern, responses in self.patterns.items():
            if re.search(pattern, user_input, re.IGNORECASE):
                response = random.choice(responses)
                self.conversation_history[-1]['bot'] = response
                return response

        # 매칭되는 패턴이 없으면 기본 응답
        response = random.choice(self.default_responses)
        self.conversation_history[-1]['bot'] = response
        return response

    def get_conversation_history(self):
        """대화 기록 반환"""
        return self.conversation_history

    def clear_history(self):
        """대화 기록 초기화"""
        self.conversation_history = []
        print("대화 기록이 초기화되었습니다.")

    def save_conversation(self, filename='conversation.txt'):
        """대화 기록을 파일로 저장"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"=== Conversation with {self.name} ===\n\n")
            for entry in self.conversation_history:
                timestamp = entry['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
                f.write(f"[{timestamp}]\n")
                f.write(f"User: {entry['user']}\n")
                f.write(f"Bot: {entry['bot']}\n\n")
        print(f"대화가 {filename}에 저장되었습니다.")

    def chat(self):
        """대화형 인터페이스"""
        print(f"=== {self.name} 챗봇 ===")
        print("대화를 시작합니다. (종료하려면 'quit' 또는 'exit' 입력)\n")

        while True:
            try:
                user_input = input("You: ").strip()

                if user_input.lower() in ['quit', 'exit', '종료']:
                    print(f"\n{self.get_response('잘가')}")

                    # 대화 기록 저장 여부 확인
                    save = input("\n대화 기록을 저장하시겠습니까? (y/n): ").lower()
                    if save == 'y':
                        self.save_conversation()
                    break

                if not user_input:
                    continue

                response = self.get_response(user_input)
                print(f"{self.name}: {response}\n")

            except KeyboardInterrupt:
                print(f"\n\n{self.name}: 대화를 종료합니다. 안녕히 가세요!")
                break
            except Exception as e:
                print(f"오류 발생: {e}")

if __name__ == '__main__':
    bot = SimpleChatbot("친구봇")
    bot.chat()
