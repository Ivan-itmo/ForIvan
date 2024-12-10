package exceptions;

public class NegativeNumberException extends Exception {
    @Override
    public String getMessage() {
        return "Введено число отрицательное";
    }
}