package entities;

import org.junit.jupiter.api.Test;

import java.util.Date;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNull;

class ResultEntryTest {

    @Test
    void constructorShouldFillAllFields() {
        Date timestamp = new Date();
        ResultEntry entry = new ResultEntry(1.0, 2.0, 3.0, true, timestamp);

        assertEquals(1.0, entry.getX());
        assertEquals(2.0, entry.getY());
        assertEquals(3.0, entry.getR());
        assertEquals(true, entry.getHit());
        assertEquals(timestamp, entry.getTimestamp());
        assertNull(entry.getId());
    }

    @Test
    void settersShouldUpdateFields() {
        Date timestamp = new Date();
        ResultEntry entry = new ResultEntry();

        entry.setId(10L);
        entry.setX(-2.0);
        entry.setY(1.5);
        entry.setR(2.5);
        entry.setHit(false);
        entry.setTimestamp(timestamp);

        assertEquals(10L, entry.getId());
        assertEquals(-2.0, entry.getX());
        assertEquals(1.5, entry.getY());
        assertEquals(2.5, entry.getR());
        assertEquals(false, entry.getHit());
        assertEquals(timestamp, entry.getTimestamp());
    }
}
