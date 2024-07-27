package com.Binfinity.Air_Quality_Backend.entity;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import java.time.LocalDateTime;

@Entity
@Table(name = "indoorairquality")
public class IndoorAirQuality {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private LocalDateTime timestamp;
    private Float co2_concentration;
    private Float pm25_concentration;
    private Float formaldehyde_concentration;
    private Float temperature;
    private Float humidity;

    // Getters and Setters
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public LocalDateTime getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(LocalDateTime timestamp) {
        this.timestamp = timestamp;
    }

    public Float getCo2_concentration() {
        return co2_concentration;
    }

    public void setCo2_concentration(Float co2_concentration) {
        this.co2_concentration = co2_concentration;
    }

    public Float getPm25_concentration() {
        return pm25_concentration;
    }

    public void setPm25_concentration(Float pm25_concentration) {
        this.pm25_concentration = pm25_concentration;
    }

    public Float getFormaldehyde_concentration() {
        return formaldehyde_concentration;
    }

    public void setFormaldehyde_concentration(Float formaldehyde_concentration) {
        this.formaldehyde_concentration = formaldehyde_concentration;
    }

    public Float getTemperature() {
        return temperature;
    }

    public void setTemperature(Float temperature) {
        this.temperature = temperature;
    }

    public Float getHumidity() {
        return humidity;
    }

    public void setHumidity(Float humidity) {
        this.humidity = humidity;
    }
}
