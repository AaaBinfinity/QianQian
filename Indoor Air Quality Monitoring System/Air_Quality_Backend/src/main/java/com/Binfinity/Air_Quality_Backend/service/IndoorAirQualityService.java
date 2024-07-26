package com.Binfinity.Air_Quality_Backend.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;
import java.util.Optional;
import com.Binfinity.Air_Quality_Backend.entity.IndoorAirQuality;
import com.Binfinity.Air_Quality_Backend.repository.IndoorAirQualityRepository;

@Service
public class IndoorAirQualityService {
    @Autowired
    private IndoorAirQualityRepository repository;

    public List<IndoorAirQuality> getAllData() {
        return repository.findAll();
    }

    public Optional<IndoorAirQuality> getDataById(Long id) {
        return repository.findById(id);
    }

    public IndoorAirQuality saveData(IndoorAirQuality data) {
        return repository.save(data);
    }

    public IndoorAirQuality updateData(Long id, IndoorAirQuality newData) {
        return repository.findById(id).map(data -> {
            data.setTimestamp(newData.getTimestamp());
            data.setCo2_concentration(newData.getCo2_concentration());
            data.setPm25_concentration(newData.getPm25_concentration());
            data.setFormaldehyde_concentration(newData.getFormaldehyde_concentration());
            data.setTemperature(newData.getTemperature());
            data.setHumidity(newData.getHumidity());
            return repository.save(data);
        }).orElseGet(() -> {
            newData.setId(id);
            return repository.save(newData);
        });
    }

    public void deleteData(Long id) {
        repository.deleteById(id);
    }
}
