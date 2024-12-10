package household;

public enum Item {
    BOAT(80),
    GOAT(50),
    CORN(100),
    COW(120),
    WIFE(60);
    private int mas;
    Item(int mas) {
        this.mas = mas;
    }
    public int getMas() {
        return mas;
    }

}

