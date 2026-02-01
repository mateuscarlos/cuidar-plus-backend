from datetime import date
from unittest.mock import Mock, patch
from uuid import uuid4

from src.application.use_cases.patients.list_patients import ListPatientsByCaregiverUseCase
from src.domain.entities.patient import Patient
from src.domain.value_objects.cpf import CPF


class TestListPatientsByCaregiverUseCase:
    def test_should_list_patients_correctly(self):
        # Arrange
        mock_repository = Mock()
        use_case = ListPatientsByCaregiverUseCase(mock_repository)
        caregiver_id = uuid4()

        # Create a mock patient
        patient = Patient(
            id=uuid4(),
            caregiver_id=caregiver_id,
            full_name="John Doe",
            cpf=CPF("52998224725"),
            date_of_birth=date(1950, 1, 1),
            gender="M",
            address="Addr",
            phone="123",
            emergency_contact="EC",
            emergency_phone="123",
            is_active=True
        )

        mock_repository.find_by_caregiver.return_value = [patient]

        # Act
        output = use_case.execute(caregiver_id)

        # Assert
        assert output.total == 1
        assert output.patients[0].id == patient.id
        assert output.patients[0].full_name == "John Doe"
        # Verify age is calculated
        assert isinstance(output.patients[0].age, int)

        mock_repository.find_by_caregiver.assert_called_once_with(caregiver_id)

    @patch('src.application.use_cases.patients.list_patients.date')
    def test_should_pass_today_to_get_age(self, mock_date):
        # Arrange
        mock_repository = Mock()
        use_case = ListPatientsByCaregiverUseCase(mock_repository)
        caregiver_id = uuid4()

        fixed_today = date(2023, 10, 1)
        mock_date.today.return_value = fixed_today

        # Create a mock patient
        # We can spy on the patient instance if we want to verify get_age is called with today
        # But Patient is a dataclass, so methods are bound.
        # We can create a real patient and patch get_age on the class or instance.

        patient = Patient(
            id=uuid4(),
            caregiver_id=caregiver_id,
            full_name="John Doe",
            cpf=CPF("52998224725"),
            date_of_birth=date(1950, 1, 1),
            gender="M",
            address="Addr",
            phone="123",
            emergency_contact="EC",
            emergency_phone="123",
            is_active=True
        )

        # Mock get_age on this instance
        patient.get_age = Mock(return_value=73)

        mock_repository.find_by_caregiver.return_value = [patient]

        # Act
        use_case.execute(caregiver_id)

        # Assert
        patient.get_age.assert_called_once_with(fixed_today)
