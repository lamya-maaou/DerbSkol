class Student {
  final String id;
  final String firstName;
  final String lastName;
  final DateTime birthDate;
  final String gender;
  final String address;
  final String parentName;
  final String parentPhone;
  final String parentEmail;
  final String className;
  final String? photoUrl;
  final DateTime registrationDate;
  final String status; // 'active', 'inactive', 'graduated', 'transferred'
  final Map<String, dynamic>? additionalInfo;

  Student({
    required this.id,
    required this.firstName,
    required this.lastName,
    required this.birthDate,
    required this.gender,
    required this.address,
    required this.parentName,
    required this.parentPhone,
    required this.parentEmail,
    required this.className,
    this.photoUrl,
    required this.registrationDate,
    this.status = 'active',
    this.additionalInfo,
  });

  // Convertir un Student en Map pour la base de données
  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'firstName': firstName,
      'lastName': lastName,
      'birthDate': birthDate.toIso8601String(),
      'gender': gender,
      'address': address,
      'parentName': parentName,
      'parentPhone': parentPhone,
      'parentEmail': parentEmail,
      'className': className,
      'photoUrl': photoUrl,
      'registrationDate': registrationDate.toIso8601String(),
      'status': status,
      'additionalInfo': additionalInfo,
    };
  }

  // Créer un Student à partir d'un Map
  factory Student.fromMap(Map<String, dynamic> map) {
    return Student(
      id: map['id'],
      firstName: map['firstName'],
      lastName: map['lastName'],
      birthDate: DateTime.parse(map['birthDate']),
      gender: map['gender'],
      address: map['address'],
      parentName: map['parentName'],
      parentPhone: map['parentPhone'],
      parentEmail: map['parentEmail'],
      className: map['className'],
      photoUrl: map['photoUrl'],
      registrationDate: DateTime.parse(map['registrationDate']),
      status: map['status'] ?? 'active',
      additionalInfo: map['additionalInfo'],
    );
  }

  // Créer une copie de l'étudiant avec des champs modifiés
  Student copyWith({
    String? id,
    String? firstName,
    String? lastName,
    DateTime? birthDate,
    String? gender,
    String? address,
    String? parentName,
    String? parentPhone,
    String? parentEmail,
    String? className,
    String? photoUrl,
    DateTime? registrationDate,
    String? status,
    Map<String, dynamic>? additionalInfo,
  }) {
    return Student(
      id: id ?? this.id,
      firstName: firstName ?? this.firstName,
      lastName: lastName ?? this.lastName,
      birthDate: birthDate ?? this.birthDate,
      gender: gender ?? this.gender,
      address: address ?? this.address,
      parentName: parentName ?? this.parentName,
      parentPhone: parentPhone ?? this.parentPhone,
      parentEmail: parentEmail ?? this.parentEmail,
      className: className ?? this.className,
      photoUrl: photoUrl ?? this.photoUrl,
      registrationDate: registrationDate ?? this.registrationDate,
      status: status ?? this.status,
      additionalInfo: additionalInfo ?? this.additionalInfo,
    );
  }
}
