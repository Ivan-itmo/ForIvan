package beans;

import entities.ResultEntry;
import javax.faces.application.FacesMessage;
import javax.faces.context.FacesContext;

public class AreaCheckBean {

    private Double x;
    private Double y;
    private Double r;

    public Double getX() { return x; }
    public void setX(Double x) { this.x = x; }

    public Double getY() { return y; }
    public void setY(Double y) { this.y = y; }

    public Double getR() { return r; }
    public void setR(Double r) { this.r = r; }

    public String checkPoint() {
        if (x == null) {
            addErrorMessage("X обязательно для заполнения.");
            return null;
        }
        if (x < -5 || x > 5) {
            addErrorMessage("X должен быть в диапазоне от -5 до 5.");
            return null;
        }

        if (y == null) {
            addErrorMessage("Y обязательно для заполнения.");
            return null;
        }
        if (y < -3.0 || y > 5.0) {
            addErrorMessage("Y должен быть в диапазоне от -3.0 до 5.0.");
            return null;
        }

        String yString = String.valueOf(y);
        if (yString.length() > 6) {
            addErrorMessage("Y не должен превышать 6 символов.");
            return null;
        }

        if (r == null) {
            addErrorMessage("R обязательно для заполнения.");
            return null;
        }
        if (r < 0.1 || r > 3.0) {
            addErrorMessage("R должен быть в диапазоне от 0.1 до 3.0.");
            return null;
        }

        boolean hit = isHit(x, y, r);

        FacesContext context = FacesContext.getCurrentInstance();
        ResultsBean resultsBean = (ResultsBean) context.getExternalContext()
                .getSessionMap()
                .get("resultsBean");

        if (resultsBean != null) {
            resultsBean.addResult(new ResultEntry(x, y, r, hit, new java.util.Date()));
        }

        return null;
    }

    private boolean isHit(Double x, Double y, Double r) {
        boolean inQuarterCircle = (x <= 0 && y <= 0 && (x * x + y * y) <= r * r);
        boolean inRectangle = (x <= r && x >= 0 && y <= r / 2.0 && y >= 0);
        boolean inTriangle = (x <= 0 && y >= 0 && y <= 2 * x + r);
        return inQuarterCircle || inRectangle || inTriangle;
    }

    private void addErrorMessage(String message) {
        FacesContext.getCurrentInstance().addMessage(
                null,
                new FacesMessage(FacesMessage.SEVERITY_ERROR, message, null)
        );
    }
}