import sympy as sp
import copy


class RouthStabilitySolver():
    __ε = sp.symbols('ε')
    __X = sp.symbols('X')
    __infinity = int(1e5)
    __neg_infinity = -__infinity
    __s = sp.symbols('s')

    __superscript_map = {
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
        return ''.join(RouthStabilitySolver.__superscript_map[d] for d in str(num))

    def __init__(self, coeffs = []):
        self.__coeffs = coeffs
        self.__order = len(coeffs) - 1
        self.__steps = []
        self.__routh_table = None

    @property
    def steps(self):
        return self.__steps


    def set_coeffs(self, coeffs):
        self.__coeffs = coeffs
        self.__order = len(coeffs) - 1
        self.__var_col = []

    def __create_var_col(self):
        self.__var_col = []
        for i in range(self.__order+1):
            self.__var_col.append(f'S{RouthStabilitySolver.to_superscript(i)}')
        self.__var_col.reverse()



    def __create_table(self):

        if self.__order< 1:
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




    # Calculates the auxiliary row using previous row diffrentiating with respect to S
    def __auxiliary_row(self, row):
        power = self.__order - row
        auxiliary_row = copy.deepcopy(self.__routh_table[row,:])
        step_aux = []

        for i in range(len(auxiliary_row)):
            if auxiliary_row[i] * power>= 0 and auxiliary_row[i] !=0:

                # perform d/ds if power is >=0
                modified_aux_element = auxiliary_row[i] * power
                step_aux.append(
                    rf"\mathrm{{coeff}}\left(\frac{{d}}{{ds}} {auxiliary_row[i]}\cdot S^{power}\right) = {modified_aux_element}"
                )
                auxiliary_row[i] = modified_aux_element

            else:
                auxiliary_row[i] = 0
                step_aux.append('0')

            power-=2

        return step_aux,auxiliary_row

    def solve(self):

        if self.__order< 1:
            print("Error")
            return

        # Create Table
        self.__create_table()
        rows = self.__routh_table.rows
        cols = self.__routh_table.cols

        # Change 2nd row 1st element from 0 -> ε to avoid division by zero
        self.__routh_table[1 , 0] = RouthStabilitySolver.__ε if self.__routh_table[1,0] == 0 and rows >1 else self.__routh_table[1,0]


        # Create Step Matrix and its row count
        step = self.__routh_table.tolist()



        # Initial sign change
        sign_change = 1 if self.__routh_table[0,0] * (self.__routh_table[1,0]).subs(RouthStabilitySolver.__ε,0) < 0 else 0




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

                # Handles Limit
                final_val = sp.limit(val , RouthStabilitySolver.__ε, 0)

                limit_expr = "\\lim_{{\\varepsilon \\to 0}}" + sp.latex(val) if 'ε' in str(val) and '/' in str(val) else None


                # Adds the equation leading to the column value
                row_step.append(
                    f"\\frac{{{sp.latex(r2)} \\cdot {sp.latex(l1)} - {sp.latex(r1)} \\cdot {sp.latex(l2)}}}{{{sp.latex(r2)}}} = {limit_expr if limit_expr is not None else sp.latex(val)}"
                )



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
            elif (isinstance(self.__routh_table[row + 2,0], sp.Number) and isinstance(self.__routh_table[row ,0], sp.Number)):
                sign_change += 1 if self.__routh_table[row+2,0] * self.__routh_table[row,0] < 0 else 0




            # Handles Zero Row
            if self.__routh_table[row + 2, 0] == RouthStabilitySolver.__ε and self.__routh_table[row + 2, 1:].tolist() == [[0]*(cols - 1)]:
                row_step = []
                aux_step ,aux_row = self.__auxiliary_row(row+1)
                row_step = aux_step
                self.__routh_table[row+2 , :] = aux_row
                step[row+2][1:] = row_step
            else:
                step[row+2][1:] = row_step+[0]*(cols - len(row_step))





            # Add the step
            self.__steps.append(copy.deepcopy(step))
            step[row+2][1:] = self.__routh_table[row + 2, 0:]

        # Add the final table
        self.__steps.append(copy.deepcopy(step))


        # Build the characteristic equation
        rhp_roots = []
        characteristic_eqn = 0
        s = RouthStabilitySolver.__s
        for i , coeff in enumerate(self.__coeffs):
                characteristic_eqn+= coeff*s**(self.__order-i)




        # Extracting RHP
        if(sign_change >0):

            roots = sp.solve(characteristic_eqn , s)
            # Seperate real and imaginary parts in x+yi format
            for root in roots:
                root_eval = root.evalf()
                real_part = sp.re(root_eval)
                imag_part = sp.im(root_eval)

                if real_part > 0:
                    # Create the real + imag*i format
                    if imag_part != 0:
                        root_str = f"{sp.latex(real_part)} + ({sp.latex(imag_part)})\\cdot\\mathrm{{i}}"
                    else:
                        root_str = f"{sp.latex(real_part)}"
                    rhp_roots.append(root_str)




        return sign_change, rhp_roots , f"{sp.latex(characteristic_eqn)}=0" , self.__steps






























if __name__ == "__main__":
    solv = RouthStabilitySolver([1,2,4,4,23,5])

















