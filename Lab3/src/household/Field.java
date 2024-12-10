package household;

import godness.God;

public class Field {
    private final int fertility;
    public Field(int fertility) {
        this.fertility = fertility;
    }
    public final int fieldPerformance(int performance, int intake, God god) {
        return fertility * performance * god.buffFertility() - intake;
    }
    public final void hello(){
        System.out.println("Есть поле с плодородностью " + fertility);
    }
}
