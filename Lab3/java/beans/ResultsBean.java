package beans;

import entities.ResultEntry;

import javax.persistence.EntityManager;
import javax.persistence.Persistence;
import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;
import java.util.Date;

public class ResultsBean implements Serializable {

    private EntityManager em;
    private List<ResultEntry> results;

    private EntityManager getEntityManager() {
        if (em == null) {
            em = Persistence.createEntityManagerFactory("derby-unit").createEntityManager();
        }
        return em;
    }

    public List<ResultEntry> getResults() {
        if (results == null) {
            loadFromDatabase();
        }
        return results;
    }

    public void addResult(ResultEntry entry) {
        if (entry.getTimestamp() == null) {
            entry.setTimestamp(new Date());
        }

        try {
            getEntityManager().getTransaction().begin();
            saveToDatabase(entry);
            getEntityManager().getTransaction().commit();
            getResults().add(0, entry);
        } catch (Exception e) {
            if (getEntityManager().getTransaction().isActive()) {
                getEntityManager().getTransaction().rollback();
            }
            throw new RuntimeException("Не удалось сохранить результат", e);
        }
    }

    public Double getLastR() {
        return getResults().isEmpty() ? 1.0 : getResults().get(0).getR();
    }

    private void loadFromDatabase() {
        try {
            results = getEntityManager().createQuery(
                    "SELECT r FROM ResultEntry r ORDER BY r.timestamp DESC",
                    ResultEntry.class
            ).getResultList();
        } catch (Exception e) {
            System.err.println("Ошибка при загрузке данных из базы: " + e.getMessage());
            results = new ArrayList<>();
        }
    }

    private void saveToDatabase(ResultEntry entry) {
        getEntityManager().persist(entry);
    }
}