package com.Binfinity.Air_Quality_Backend.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import com.Binfinity.Air_Quality_Backend.entity.IndoorAirQuality;

public interface IndoorAirQualityRepository extends JpaRepository<IndoorAirQuality, Long> {
}
