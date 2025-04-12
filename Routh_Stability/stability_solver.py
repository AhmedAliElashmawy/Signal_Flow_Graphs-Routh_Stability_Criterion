import sympy as sp
import copy


class RouthStabilitySolver():
    __ε = sp.symbols('ε')
    __X = sp.symbols('X')
    __infinity = int(1e5)
    __neg_infinity = -__infinity

    superscript_map = {
    '0': '⁰',
    '1': '¹',
    '2': '²',
    '3': '³',
    '4': '⁴',
    '5': '⁵',
    '6': '⁶',
    '7': '⁷',
    '8': '⁸',
    '9': '⁹'
}
    def to_superscript(num):
        return ''.join(RouthStabilitySolver.superscript_map[d] for d in str(num))

    def __init__(self, coeffs = None):
        self.__coeffs = coeffs
        self.__order = len(coeffs) - 1
        self.__steps = []
        self.__routh_table = None


    def set_coeffs(self, coeffs):
        self.__coeffs = coeffs
        self.__order = len(coeffs) - 1

    def __create_var_col(self):
        self.__var_col = []
        for i in range(self.__order+1):
            self.__var_col.append(f'S{RouthStabilitySolver.to_superscript(i)}')
        self.__var_col.reverse()




    def create_table(self):

        if self.__order< 2:
            print("Error")
            return

        rows = self.__order +1
        cols = (rows +1)//2
        shape = (rows , cols )

        routh_table = sp.zeros(*shape)

        # Fill the first two rows of the Routh table
        for i , j  in zip(range(0,rows-1,2) , range(cols)):
            routh_table[0,j] = self.__coeffs[i]
            routh_table[1,j] = self.__coeffs[i+1]

        # Check if there is one last coefficient left (for odd-length coefficient list)
        if len(self.__coeffs) % 2 != 0:
            routh_table[0, cols - 1] = self.__coeffs[-1]

        # Fills the positions that are not trivial (needs calculations / not 0)
        for i in range(rows-2):
            for j in range(cols-1):
                if routh_table[i,j+1] != 0 or routh_table[i+1,j+1] != 0:
                    routh_table[i+2,j] = RouthStabilitySolver.__X
                else:
                    break


        self.__create_var_col()


        self.__routh_table = routh_table

    def print_steps(self):
        for x in self.__steps:
            for rows in x:
                print (rows)
            print('\n\n')


    def __auxiliary_row(self, row):
        power = self.__order - row
        auxiliary_row = copy.deepcopy(self.__routh_table[row,:])


        for i in range(len(auxiliary_row)):

            auxiliary_row[i] = max(0, auxiliary_row[i] * power)
            power-=2

        return auxiliary_row


    def solve(self):
        rows = self.__routh_table.rows
        cols = self.__routh_table.cols
        step = self.__routh_table.tolist()
        row_i = 2
        sign_change = 1 if self.__routh_table[0,0] * self.__routh_table[1,0] < 0 else 0

        for row , var in zip(step , self.__var_col):
            row.insert(0,var)

        self.__steps.append(copy.deepcopy(step))
        for row in range(self.__routh_table.rows - 2):

            r1= self.__routh_table[row,0]
            r2= self.__routh_table[row+1,0]



            row_step = []

            for col in range(self.__routh_table.cols):

                if(self.__routh_table[row + 2,col] == 0):
                    break

                l1 = self.__routh_table[row,col+1]
                l2 = self.__routh_table[row+1,col+1]

                # Calculates the value at the current col
                val = ( r2*l1 - r1*l2 ) / r2
                val = RouthStabilitySolver.__ε if val == 0 and col == 0 and row+2 !=rows-1 else val

                # Adds the equation leading to the column value
                row_step.append(str(r2) + '\u00D7' + str(l1) + '-' + str(r1) + '\u00D7' + str(l2) + '/' + str(r2) + '=' + str(val))

                # Handles Limit
                final_val = sp.limit(val , RouthStabilitySolver.__ε, 0)

                if val != RouthStabilitySolver.__ε and val != final_val:
                    row_step[-1]+=('=' + str(final_val))

                # Handles final values for limits
                if final_val == sp.oo:
                    self.__routh_table[row + 2,col] = RouthStabilitySolver.__infinity

                elif final_val == -sp.oo:
                    self.__routh_table[row + 2,col] = RouthStabilitySolver.__neg_infinity

                elif final_val == 0 and col == 0:
                    self.__routh_table[row + 2,col] = RouthStabilitySolver.__ε

                else:
                    self.__routh_table[row + 2,col] = final_val


            # Checks for sign change
            if(isinstance(self.__routh_table[row + 2,0], sp.Number) and isinstance(self.__routh_table[row + 1,0], sp.Number)):
                sign_change += 1 if self.__routh_table[row+2,0] * self.__routh_table[row+1,0] < 0 else 0





            # Handles Zero Row
            print()
            if self.__routh_table[row + 2, 0] == RouthStabilitySolver.__ε and self.__routh_table[row + 2, 1:].tolist() == [[0]*(cols - 1)]:
                row_step = [0] * cols
                step[row_i ][1:] = row_step
                row_i+=1
                self.__routh_table[row + 2, :] = self.__auxiliary_row(row+1)
                step.insert(row_i, [step[row+2][0]] + list(self.__routh_table[row + 2, :]))

            else:
                step[row_i][1:] = row_step+['0']*(cols - len(row_step))






            self.__steps.append(copy.deepcopy(step))
            step[row_i][1:] = self.__routh_table[row + 2, 0:]
            row_i+=1

        self.__steps.append(copy.deepcopy(step))


        return sign_change























if __name__ == "__main__":
    solv = RouthStabilitySolver([1,2,8,12,20,16,16])
    solv.create_table()
    sign_change=solv.solve()
    solv.print_steps()
    print(f"Sign Changes : {sign_change}")
















