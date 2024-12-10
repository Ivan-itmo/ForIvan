package characters;

import moves.Weapon;
import java.util.Objects;

public abstract class Wildman extends People{
    public Wildman(String name, int height, int weight) {
        this.name = name;
        this.height = height;
        this.weight = weight;
    }
    public abstract void setDamage(MainCharacter character);
    @Override
    public boolean equals(Object obj) {
        // Проверка на то, является ли объект сам собой
        if (this == obj) {
            return true;
        }

        // Проверка на null и на класс объекта
        if (obj == null || this.getClass() != obj.getClass()) {
            return false;
        }

        // Приведение obj к типу Wildman
        Wildman wildman = (Wildman) obj;

        // Сравнение всех полей
        return getHeight() == wildman.getHeight() &&
                getWeight() == wildman.getWeight() &&
                Objects.equals(getName(), wildman.getName());
    }

    // Переопределение hashCode()
    @Override
    public int hashCode() {
        return Objects.hash(getName(), getHeight(), getWeight()); // Сгенерировать хэш-код на основе всех полей
    }

    // Переопределение toString()
    @Override
    public String toString() {
        return "Wildman{" +
                "name='" + getName() + '\'' +
                ", height=" + getHeight() +
                ", weight=" + getWeight() +
                '}'; // Строковое представление объекта
    }
}

