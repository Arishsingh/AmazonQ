import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestHandler;
import java.util.Map;
import java.util.List;
import java.util.ArrayList;

public class SudokuLambda implements RequestHandler<Map<String, Object>, Map<String, Object>> {

    @Override
    public Map<String, Object> handleRequest(Map<String, Object> input, Context context) {
        List<List<Integer>> puzzleInput = (List<List<Integer>>) input.get("puzzle");
        int[][] sudoku = new int[9][9];

        // Convert List<List<Integer>> to int[][]
        for (int i = 0; i < 9; i++) {
            List<Integer> row = puzzleInput.get(i);
            for (int j = 0; j < 9; j++) {
                sudoku[i][j] = row.get(j);
            }
        }

        boolean solved = sudokusolver(sudoku, 0, 0);

        Map<String, Object> response = new java.util.HashMap<>();
        if (solved) {
            response.put("status", "solved");
            response.put("solution", toList(sudoku));
        } else {
            response.put("status", "unsolvable");
        }
        return response;
    }

    private List<List<Integer>> toList(int[][] board) {
        List<List<Integer>> result = new ArrayList<>();
        for (int[] row : board) {
            List<Integer> rowList = new ArrayList<>();
            for (int cell : row) {
                rowList.add(cell);
            }
            result.add(rowList);
        }
        return result;
    }

    public static boolean issafe(int[][] sudoku, int row, int col, int digit) {
        for (int i = 0; i < 9; i++) if (sudoku[i][col] == digit) return false;
        for (int j = 0; j < 9; j++) if (sudoku[row][j] == digit) return false;
        int sr = (row / 3) * 3, sc = (col / 3) * 3;
        for (int i = sr; i < sr + 3; i++)
            for (int j = sc; j < sc + 3; j++)
                if (sudoku[i][j] == digit) return false;
        return true;
    }

    public static boolean sudokusolver(int[][] sudoku, int row, int col) {
        if (row == 9) return true;
        int nextRow = row, nextCol = col + 1;
        if (col + 1 == 9) {
            nextRow = row + 1;
            nextCol = 0;
        }
        if (sudoku[row][col] != 0) {
            return sudokusolver(sudoku, nextRow, nextCol);
        }
        for (int digit = 1; digit <= 9; digit++) {
            if (issafe(sudoku, row, col, digit)) {
                sudoku[row][col] = digit;
                if (sudokusolver(sudoku, nextRow, nextCol)) return true;
                sudoku[row][col] = 0;
            }
        }
        return false;
    }
    public static void main(String args[]){
        {
            "puzzle": [
              [5,3,0,0,7,0,0,0,0],
              [6,0,0,1,9,5,0,0,0],
              [0,9,8,0,0,0,0,6,0],
              [8,0,0,0,6,0,0,0,3],
              [4,0,0,8,0,3,0,0,1],
              [7,0,0,0,2,0,0,0,6],
              [0,6,0,0,0,0,2,8,0],
              [0,0,0,4,1,9,0,0,5],
              [0,0,0,0,8,0,0,7,9]
            ]
          }
          
    }
}

