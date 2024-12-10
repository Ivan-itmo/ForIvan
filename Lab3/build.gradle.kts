plugins {
    id("java")  // Указывает, что это Java проект
}

repositories {
    mavenCentral()  // Это стандартный репозиторий, откуда Gradle будет искать зависимости (для будущих нужд или библиотек)
}

dependencies {
    // Здесь могут быть указаны зависимости, если они появятся
}

java {
    sourceCompatibility = JavaVersion.VERSION_17  // Указание версии JDK, которую вы используете
    targetCompatibility = JavaVersion.VERSION_17  // Версия компиляции
}