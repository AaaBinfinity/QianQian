package com.Binfinity.Air_Quality_Backend.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;
import java.util.Optional;
import com.Binfinity.Air_Quality_Backend.entity.IndoorAirQuality;
import com.Binfinity.Air_Quality_Backend.service.IndoorAirQualityService;

@RestController
@RequestMapping("/api/airquality")
public class IndoorAirQualityController {
    @Autowired
    private IndoorAirQualityService service;

    @GetMapping("/data")
    public List<IndoorAirQuality> getAllData() {
        return service.getAllData();
    }

    @GetMapping("/data/{id}")
    public ResponseEntity<IndoorAirQuality> getDataById(@PathVariable Long id) {
        Optional<IndoorAirQuality> data = service.getDataById(id);
        return data.map(ResponseEntity::ok).orElseGet(() -> ResponseEntity.notFound().build());
    }

    @PostMapping("/data")
    public IndoorAirQuality createData(@RequestBody IndoorAirQuality data) {
        return service.saveData(data);
    }

    @PutMapping("/data/{id}")
    public ResponseEntity<IndoorAirQuality> updateData(@PathVariable Long id, @RequestBody IndoorAirQuality newData) {
        Optional<IndoorAirQuality> updatedData = Optional.ofNullable(service.updateData(id, newData));
        return updatedData.map(ResponseEntity::ok).orElseGet(() -> ResponseEntity.notFound().build());
    }

    @DeleteMapping("/data/{id}")
    public ResponseEntity<Void> deleteData(@PathVariable Long id) {
        service.deleteData(id);
        return ResponseEntity.noContent().build();
    }
}
