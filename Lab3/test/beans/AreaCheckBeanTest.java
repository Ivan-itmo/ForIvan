package beans;

import org.junit.jupiter.api.Test;

import java.lang.reflect.Method;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class AreaCheckBeanTest {

    @Test
    void shouldReturnTrueForPointInsideQuarterCircle() throws Exception {
        assertTrue(invokeIsHit(-1.0, -1.0, 2.0));
    }

    @Test
    void shouldReturnTrueForPointInsideRectangle() throws Exception {
        assertTrue(invokeIsHit(1.0, 0.5, 2.0));
    }

    @Test
    void shouldReturnTrueForPointInsideTriangle() throws Exception {
        assertTrue(invokeIsHit(-1.0, 0.5, 3.0));
    }

    @Test
    void shouldReturnTrueForPointOnBoundary() throws Exception {
        assertTrue(invokeIsHit(0.0, -2.0, 2.0));
    }

    @Test
    void shouldReturnFalseForPointOutsideArea() throws Exception {
        assertFalse(invokeIsHit(2.0, 2.0, 1.0));
    }

    private boolean invokeIsHit(Double x, Double y, Double r) throws Exception {
        AreaCheckBean bean = new AreaCheckBean();
        Method method = AreaCheckBean.class.getDeclaredMethod("isHit", Double.class, Double.class, Double.class);
        method.setAccessible(true);
        return (boolean) method.invoke(bean, x, y, r);
    }
}
