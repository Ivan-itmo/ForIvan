package mbeans;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

class AreaTest {

    @Test
    void shouldCalculateAreaForRadius() {
        Area area = new Area();

        area.updateRadius(2.0);

        double expected = Math.PI + 2.0 + 1.0;
        assertEquals(expected, area.getArea(), 1e-9);
        assertEquals(2.0, area.getCurrentR(), 1e-9);
    }
}
