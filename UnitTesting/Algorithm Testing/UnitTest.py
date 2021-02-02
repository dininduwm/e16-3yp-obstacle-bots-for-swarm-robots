import random
from main import Test
from robot import robot

ARENA_DIM = 30


class testObj:

    def __init__(self, no_of_robots):
        self.no_of_robots = no_of_robots
        self.no_of_collisions = 0
        self.unstable_destinations = 0
        self.out_of_the_board = 0
        self.passed = False
        global results

    def test(self):
        data_list = []

        dic_position_start = set()
        dic_position_end = set()

        start_pos = (1,1)
        end_pos = (29,29)
        for i in range(self.no_of_robots):
            while(start_pos in dic_position_start):
                start_pos = (random.randint(2, ARENA_DIM - 2), random.randint(2, ARENA_DIM - 2))
            while(end_pos in dic_position_end):
                end_pos = (random.randint(2, ARENA_DIM-2 ),random.randint(2, ARENA_DIM-2))
            data_list.append(
                robot(
                    start_pos,
                    0,
                    end_pos,
                    0
                )
            )
            dic_position_start.add(start_pos)
            dic_position_end.add(end_pos)

        Test(data_list, self)

        try:
            assert (self.no_of_collisions <= 1)
            assert (self.unstable_destinations <= 1)
            assert (self.out_of_the_board <= 1)
            self.passed = True
        except AssertionError:
            self.passed = False


    def show_test_results(self):

        for i in range(len(results)):

            print(f'\n***************Test case {i+1} results ****************')
            print(f"Test case executed with {results[i].no_of_robots} robots.")
            print("Number of collisions : ", results[i].no_of_collisions)
            print("Unstable destinations : ", results[i].unstable_destinations)
            print("Out of the area : ", results[i].out_of_the_board)

            if results[i].passed:
                print("Great! Test passed.")
            else:
                print("Oops! Test Failed.")

if __name__ == "__main__":

    results = []

    no_of_test_cases = 10

    for i in range(no_of_test_cases):
        test_case = testObj(random.randint(3, 20))
        test_case.test()
        results.append(test_case)
        test_case.show_test_results()

    cnt = 0
    for item in results:
        if item.passed:
            cnt += 1
    
    print("\n**************** Overall statistics ******************\n")
    print(" " * 15, cnt, "Passed!.")
    print(" " * 15, no_of_test_cases - cnt, "Failed!.\n")  
    print("*" * 55)
    
