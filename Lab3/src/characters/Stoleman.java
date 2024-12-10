package characters;
import java.util.Objects;
import household.*;

public class Stoleman extends People{
    private final int maxmas;
    public Stoleman(String name, int height, int weight, int maxmas) {
        this.name = name;
        this.height = height;
        this.weight = weight;
        this.maxmas = maxmas;
    }
    @Override
    public final void hello(){
        System.out.println("Появился воришка из племени " + getName() + " который может унести вес " + maxmas + "!");
    }
    public final int getMaxmas() {
        return maxmas;
    }
    public final void processStole(MainCharacter character, CharacterItems property) {
        if (character.getLive()) {
            int c = 0;
            for (Item prop : property.getProperty()) {
                if (prop.getMas() > maxmas) {
                    c += 1;
                }
            }
            Item[] newproperty = new Item[c];
            int i = 0;
            for (Item prop : property.getProperty()) {
                if (prop.getMas() > maxmas) {
                    newproperty[i++] = prop;
                }
                else{
                    System.out.println("Воришка " + getName() + " украл " + prop);
                }
            }
            property.setProperty(newproperty);
        }
    }
    @Override
    public boolean equals(Object obj) {
        if (this == obj) {
            return true; // Сравниваем ссылки: если это один и тот же объект, возвращаем true
        }
        if (obj == null || this.getClass() != obj.getClass()) {
            return false; // Если другой объект null или классы не совпадают, возвращаем false
        }
        Stoleman stoleman = (Stoleman) obj; // Приводим объект к классу Stoleman
        return maxmas == stoleman.maxmas &&
                getHeight() == stoleman.getHeight() &&
                getWeight() == stoleman.getWeight() &&
                getName().equals(stoleman.getName());
    }

    @Override
    public int hashCode() {
        // Генерируем хэш-код на основе всех полей
        return Objects.hash(getName(), getHeight(), getWeight(), maxmas);
    }

    @Override
    public String toString() {
        return "Stoleman{" +
                "name='" + getName() + '\'' +
                ", height=" + getHeight() +
                ", weight=" + getWeight() +
                ", maxmas=" + maxmas +
                '}';
    }


}