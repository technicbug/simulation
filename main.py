import random
import matplotlib.pyplot as plt
import math

conserve = 0.6  #음식 보존율
MORTALITY_RATE = 0.1
CRETURE_NUMBER = 10
# Creature 클래스 정의
class Creature:
    def __init__(self, trait):
        self.trait = trait  # 'A', 'B', 'C' 중 하나
        self.alive = True   # 생존 여부
        self.templive = True
        self.food = 0       # 먹이를 먹은 횟수

# 싸움 및 먹이 처리 함수
def fight(creature1, creature2):
    # A vs A: 둘 다 죽음
    if creature1.trait == 'A' and creature2.trait == 'A':
        
        creature1.alive = False
        creature2.alive = False

        return 1  # 먹이 소모 1

    # A vs B: 70% A 승리, 30% B 승리
    elif creature1.trait == 'A' and creature2.trait == 'B':
        if random.random() < 0.6:
            creature2.alive = False  # A 승리
            creature1.food += 1
        else:
            creature1.alive = False  # B 승리
            creature2.food += 1
        return 1  # 하나의 먹이 소모

    elif creature1.trait == 'B' and creature2.trait == 'A':
        if random.random() < 0.6:
            creature1.alive = False  # B 승리
            creature2.food += 1
        else:
            creature2.alive = False  # A 승리
            creature1.food += 1
        return 1

    # A vs C: A가 먹이를 빼앗음
    elif creature1.trait == 'A' and creature2.trait == 'C':
        creature1.food += 1
        creature2.templive = False
        return 1  # 하나의 먹이 소모

    elif creature1.trait == 'C' and creature2.trait == 'A':
        creature2.food += 1
        creature1.templive = False
        return 1

    # B vs B: 싸워서 먹이를 나누어 먹고 50% 생존
    elif creature1.trait == 'B' and creature2.trait == 'B':
        if random.random() < 0.5:
            creature1.alive = False
        else:
            creature1.food += 1
            creature2.alive = False

        if random.random() < 0.5:
            creature1.food += 1
            creature2.alive = False
        else:
            creature2.food += 1
            creature2.alive = False
        
        
        
        
        return 1  # 하나의 먹이 소모

    # B vs C: B가 먹이를 먹음, C는 새로운 먹이를 찾아야 함
    elif creature1.trait == 'B' and creature2.trait == 'C':
        creature1.food += 1
        creature2.templive = False
        return 1  # 하나의 먹이 소모

    elif creature1.trait == 'C' and creature2.trait == 'B':
        creature2.food += 1
        creature1.templive = False
        return 1

    # C vs C: 둘 다 먹이를 나누어 먹음
    elif creature1.trait == 'C' and creature2.trait == 'C':
        creature1.food += 1
        creature2.food += 1
        return 2  # 두 개의 먹이 소모

    return 0  # 싸움이 일어나지 않음
# 남은 먹이를 C형 개체들에게 분배하는 함수
def handle_remaining_food(C_creatures, remaining_food):
    if remaining_food >= len(C_creatures):
        # 남은 먹이가 충분하면 모두 먹고 생존
        for creature in C_creatures:
            creature.food += 1
            creature.templive = True
        return 0  # 남은 먹이를 모두 소비
    else:
        # 먹이가 부족하면 일부 C형 개체만 생존
        # 남은 먹이 수만큼 랜덤하게 C형 개체들 중 일부를 선택
        if remaining_food > 0:
            food_for_C = math.ceil(remaining_food)
            survivors = random.sample(C_creatures, food_for_C)
            for creature in survivors:
                creature.food += 1
                creature.templive = True

            for creature in C_creatures:
                if creature not in survivors:
                    creature.alive = False
        # 먹이가 하나도 없을 때는 모두 사망 처리
        else:
            for creature in C_creatures:
                creature.alive = False
        return 0  # 남은 먹이가 모두 소모됨


# 세대별 시뮬레이션 함수
def run_simulation(creatures):
    # 현재 살아있는 A, B, C형 개체 분류
    A_creatures = [c for c in creatures if c.trait == 'A' and c.alive]
    B_creatures = [c for c in creatures if c.trait == 'B' and c.alive]
    C_creatures = [c for c in creatures if c.trait == 'C' and c.alive]

    # 현재 살아있는 모든 개체 수
    total_creatures = len(A_creatures) + len(B_creatures) + len(C_creatures)
    print(f'총 개체수 : {total_creatures}')
    if total_creatures == 0:
        return

    # 각 세대에서 총 먹이 수는 살아있는 개체 수과 비슷하게 설정 (±2 범위 내 랜덤)
    total_food = random.randint(max(1,math.ceil(total_creatures*0.7)), math.ceil(total_creatures*0.8))
    # total_food = 10
    
    print(f"이번 세대에 할당된 먹이 수: {total_food}")

    # 1차적으로 먹이 소비 (A vs A, A vs B, B vs B, A vs C, B vs C, C vs C)
    # 개체들을 랜덤하게 섞어서 싸움을 시뮬레이션
    random.shuffle(creatures)
    used_food = 0
    for i in range(0, len(creatures), 2):
        if i + 1 < len(creatures):
            used_food += fight(creatures[i], creatures[i+1])
        
        # 사용된 먹이가 총 먹이보다 커지면 먹이 소모를 멈춤
        if used_food >= total_food:
            used_food = total_food
            break

    # 남은 먹이 계산
    remaining_food = total_food - used_food
    print(remaining_food)
    # C형 개체가 남은 먹이를 찾아먹도록 처리
    C_temp = [c for c in creatures if c.trait == 'C' and c.templive == False and c.alive == True]
    if C_temp:
        handle_remaining_food(C_temp, math.ceil(remaining_food*conserve))

# 시각화 함수: 세대별 개체 수 변화를 그래프로 표시
def visualize_population(population_history):
    generations = list(range(1, len(population_history) + 1))
    A_population = [pop['A'] for pop in population_history]
    B_population = [pop['B'] for pop in population_history]
    C_population = [pop['C'] for pop in population_history]

    plt.figure(figsize=(10, 6))
    plt.plot(generations, A_population, label="A", marker='o')
    plt.plot(generations, B_population, label="B", marker='s')
    plt.plot(generations, C_population, label="C", marker='^')
    plt.xlabel("gen")
    plt.ylabel("population")
    plt.title("Changes in the number of individuals with each tendency by generation")
    plt.legend()
    plt.grid(True)
    plt.xticks(generations)
    plt.show()

# 전체 시뮬레이션 실행
def simulate(generations, n_offspring):
    # 초기 개체군: A형, B형, C형 각 10마리씩
    creatures = [Creature('A') for _ in range(CRETURE_NUMBER)] + \
                [Creature('B') for _ in range(CRETURE_NUMBER)] + \
                [Creature('C') for _ in range(CRETURE_NUMBER)]

    population_history = []

    for generation in range(generations):
        print(f"\n=== 세대 {generation + 1} ===")

        for creature in creatures:
            creature.food = 0

        run_simulation(creatures)

        

        # 각 세대별 개체 수 기록
        A_count = sum(1 for c in creatures if c.trait == 'A' and c.alive)
        B_count = sum(1 for c in creatures if c.trait == 'B' and c.alive)
        C_count = sum(1 for c in creatures if c.trait == 'C' and c.alive)


        if A_count == 0 and B_count == 0 and C_count == 0:
            print("모든 개체가 죽었습니다. 시뮬레이션 종료.")
            break

        for creature in creatures:
            if creature.food == 0:
                creature.alive = False
        

        # 번식을 통해 자손 추가
        new_creatures = []
        for creature in creatures:
            if creature.alive and (creature.trait in ['A', 'B', 'C']):
                for _ in range(n_offspring):
                    new_creatures.append(Creature(creature.trait))
        creatures.extend(new_creatures)

        for creature in creatures:
            if creature.alive and random.random() < MORTALITY_RATE:
                creature.alive = False

        creatures = [creature for creature in creatures if creature.alive]

        print(f"번식 후 개체 수: {len(creatures)}")
        A_count = sum(1 for c in creatures if c.trait == 'A' and c.alive)
        B_count = sum(1 for c in creatures if c.trait == 'B' and c.alive)
        C_count = sum(1 for c in creatures if c.trait == 'C' and c.alive)
        population_history.append({'A': A_count, 'B': B_count, 'C': C_count})

        print(f"A형: {A_count}, B형: {B_count}, C형: {C_count}")

        # 다음 세대로 진행하기 위해 Enter 키 입력 대기
        input("다음 세대로 진행하려면 Enter 키를 누르세요...")

    # 시각화
    visualize_population(population_history)

# 테스트 실행 (10세대, 각 생존 개체당 2마리의 자손)
if __name__ == "__main__":
    generations = int(input("시뮬레이션할 세대수 : "))    # 시뮬레이션할 세대 수
    n_offspring = int(input('성장률(살아남은 개체가 낳는 자손 수) : '))     # 각 살아남은 개체가 낳는 자손 수
    simulate(generations, n_offspring)
