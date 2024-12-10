package characters;

public abstract class People {
    protected String name;
    protected int height;
    protected int weight;
    public abstract void hello();

    public final String getName(){
        return name;
    }
    public final int getHeight(){
        return height;
    }
    public final int getWeight(){
        return weight;
    }
}
