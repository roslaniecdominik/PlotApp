def solution_generator(solution_code):
            from itertools import combinations
            solutions = ["GPS", "GLONASS", "GALILEO", "BeiDou", "IRNSS", "SBAS"]
            map = {}

            for i in range(1, len(solutions) + 1):
                for ones_position in combinations(range(6), i):
                    code = ["0"] * 6
                    for position in ones_position:
                        code[position] = "1"
                    code = "".join(code)
                    
                    right_letters = ", ".join(solutions[position] for position in ones_position)
                    map[code] = right_letters
                    map[right_letters] = code
        
            return map.get(solution_code, "WRONG CODE")