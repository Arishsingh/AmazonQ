import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestHandler;
import java.util.Map;

public class SudokuLambda implements RequestHandler<Map<String, Object>, String> {
    @Override
    public String handleRequest(Map<String, Object> input, Context context) {
        context.getLogger().log("Sudoku Lambda invoked");
        return "Hello from Sudoku Lambda!";
    }
}
