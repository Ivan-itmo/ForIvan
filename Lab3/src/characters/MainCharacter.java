package characters;
import household.*;
import godness.God;
import java.util.Objects;

public class MainCharacter extends People{
    private int health;
    private final int performance;
    private final int intake;
    private boolean live = true;
    public MainCharacter(String name, int height, int weight, int health, int performance, int intake) {
        this.name = name;
        this.height = height;
        this.weight = weight;
        this.health = health;
        this.performance = performance;
        this.intake = intake;
    }
    @Override
    public final void hello(){
        System.out.println("Появился главный персонаж " + getName() + "!");
    }
    public final boolean getLive() {
        return live;
    }
    public final void starvation(Field field, God god){
        if (field.fieldPerformance(performance, intake, god) < 0){
            health += field.fieldPerformance(performance, intake, god);
            if (health <= 0){
                live = false;
                System.out.println(getName() + " погиб от голода");
            }
        }
        else{
            System.out.println("Год прошел без голода");
        }
    }
    public final void takeDamage(int attack, String nameattacker){
        if (getLive()) {
            health -= attack;
            if (health <= 0) {
                live = false;
                System.out.println(getName() + " погиб от рук " + nameattacker);
            }
            else {
                System.out.println("Получен дамаг " + getName() + " на " + attack + " от " + nameattacker + " оставшееся здоровье " + health);
            }
        }
    }
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true; // Проверяем, ссылаются ли объекты на одну и ту же память
        if (obj == null || this.getClass() != obj.getClass()) return false; // Проверяем, что объект не null и того же класса

        MainCharacter that = (MainCharacter) obj;
        return health == that.health &&
                performance == that.performance &&
                intake == that.intake &&
                getName().equals(that.getName()) && // Сравниваем строку имени
                getHeight() == that.getHeight() &&
                getWeight() == that.getWeight();
    }

    @Override
    public int hashCode() {
        return Objects.hash(getName(), getHeight(), getWeight(), health, performance, intake);
    }

    @Override
    public String toString() {
        return "MainCharacter{" +
                "name='" + getName() + '\'' +
                ", height=" + getHeight() +
                ", weight=" + getWeight() +
                ", health=" + health +
                ", performance=" + performance +
                ", intake=" + intake +
                '}';
    }

}
