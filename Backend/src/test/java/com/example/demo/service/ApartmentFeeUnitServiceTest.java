package com.example.demo.service;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import com.example.demo.entity.ApartmentFeeUnit;
import com.example.demo.repository.ApartmentFeeUnitRepository;
import java.util.Optional;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class ApartmentFeeUnitServiceTest {

    @Mock
    private ApartmentFeeUnitRepository feeUnitRepository;

    @InjectMocks
    private ApartmentFeeUnitService feeUnitService;

    @Test
    void getFeeUnit_createsDefaultWhenMissing() {
        when(feeUnitRepository.findById(1L)).thenReturn(Optional.empty());
        when(feeUnitRepository.save(any(ApartmentFeeUnit.class)))
                .thenAnswer(invocation -> invocation.getArgument(0));

        ApartmentFeeUnit result = feeUnitService.getFeeUnit();

        assertNotNull(result);
        assertEquals(1L, result.getId());
        assertEquals(300000L, result.getApartmentPricePerM2());
        assertEquals(15000L, result.getServiceFeePerM2());
        assertEquals(15000L, result.getWaterFeePerM3());
        assertEquals(3500L, result.getElectricityFeePerKWh());
        assertEquals(0L, result.getParkingFeePerMonth());
        assertEquals(0L, result.getParkingFeePerHour());
        verify(feeUnitRepository).save(any(ApartmentFeeUnit.class));
    }

    @Test
    void getFeeUnit_fillsNullParkingFeesOnLegacyRecord() {
        ApartmentFeeUnit legacy = new ApartmentFeeUnit();
        legacy.setId(1L);
        legacy.setApartmentPricePerM2(250000L);
        legacy.setParkingFeePerMonth(null);
        legacy.setParkingFeePerHour(null);

        when(feeUnitRepository.findById(1L)).thenReturn(Optional.of(legacy));
        when(feeUnitRepository.save(any(ApartmentFeeUnit.class)))
                .thenAnswer(invocation -> invocation.getArgument(0));

        ApartmentFeeUnit result = feeUnitService.getFeeUnit();

        assertEquals(0L, result.getParkingFeePerMonth());
        assertEquals(0L, result.getParkingFeePerHour());
        verify(feeUnitRepository).save(legacy);
    }

    @Test
    void getFeeUnit_returnsExistingRecordWithoutSavingWhenComplete() {
        ApartmentFeeUnit existing = new ApartmentFeeUnit();
        existing.setId(1L);
        existing.setParkingFeePerMonth(100000L);
        existing.setParkingFeePerHour(5000L);

        when(feeUnitRepository.findById(1L)).thenReturn(Optional.of(existing));

        ApartmentFeeUnit result = feeUnitService.getFeeUnit();

        assertEquals(100000L, result.getParkingFeePerMonth());
        assertEquals(5000L, result.getParkingFeePerHour());
        verify(feeUnitRepository, never()).save(any());
    }

    @Test
    void saveFeeUnit_defaultsNullParkingFeesBeforeSaving() {
        ApartmentFeeUnit unit = new ApartmentFeeUnit();
        unit.setId(1L);
        unit.setParkingFeePerMonth(null);
        unit.setParkingFeePerHour(null);

        when(feeUnitRepository.save(any(ApartmentFeeUnit.class)))
                .thenAnswer(invocation -> invocation.getArgument(0));

        ApartmentFeeUnit saved = feeUnitService.saveFeeUnit(unit);

        assertEquals(0L, saved.getParkingFeePerMonth());
        assertEquals(0L, saved.getParkingFeePerHour());
        verify(feeUnitRepository).save(unit);
    }
}
