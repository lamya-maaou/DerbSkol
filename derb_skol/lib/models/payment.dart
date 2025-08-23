import 'package:flutter/foundation.dart';

class Payment {
  final String id;
  final String studentId; // Référence à l'étudiant
  final double amount;
  final DateTime paymentDate;
  final String paymentMethod; // 'cash', 'check', 'bank_transfer', 'card', 'other'
  final String? transactionId;
  final String? description;
  final String status; // 'pending', 'completed', 'failed', 'refunded'
  final String? receivedBy; // ID de l'utilisateur qui a enregistré le paiement
  final String? notes;
  final String? receiptNumber;
  final String? academicYear;
  final String? term; // '1er trimestre', '2ème trimestre', '3ème trimestre', 'annuel'
  final String? invoiceId; // Référence à la facture associée

  Payment({
    required this.id,
    required this.studentId,
    required this.amount,
    required this.paymentDate,
    required this.paymentMethod,
    this.transactionId,
    this.description,
    this.status = 'completed',
    this.receivedBy,
    this.notes,
    this.receiptNumber,
    this.academicYear,
    this.term,
    this.invoiceId,
  });

  // Convertir un Payment en Map pour la base de données
  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'studentId': studentId,
      'amount': amount,
      'paymentDate': paymentDate.toIso8601String(),
      'paymentMethod': paymentMethod,
      'transactionId': transactionId,
      'description': description,
      'status': status,
      'receivedBy': receivedBy,
      'notes': notes,
      'receiptNumber': receiptNumber,
      'academicYear': academicYear,
      'term': term,
      'invoiceId': invoiceId,
    };
  }

  // Créer un Payment à partir d'un Map
  factory Payment.fromMap(Map<String, dynamic> map) {
    return Payment(
      id: map['id'],
      studentId: map['studentId'],
      amount: (map['amount'] as num).toDouble(),
      paymentDate: DateTime.parse(map['paymentDate']),
      paymentMethod: map['paymentMethod'],
      transactionId: map['transactionId'],
      description: map['description'],
      status: map['status'] ?? 'completed',
      receivedBy: map['receivedBy'],
      notes: map['notes'],
      receiptNumber: map['receiptNumber'],
      academicYear: map['academicYear'],
      term: map['term'],
      invoiceId: map['invoiceId'],
    );
  }

  // Créer une copie du paiement avec des champs modifiés
  Payment copyWith({
    String? id,
    String? studentId,
    double? amount,
    DateTime? paymentDate,
    String? paymentMethod,
    String? transactionId,
    String? description,
    String? status,
    String? receivedBy,
    String? notes,
    String? receiptNumber,
    String? academicYear,
    String? term,
    String? invoiceId,
  }) {
    return Payment(
      id: id ?? this.id,
      studentId: studentId ?? this.studentId,
      amount: amount ?? this.amount,
      paymentDate: paymentDate ?? this.paymentDate,
      paymentMethod: paymentMethod ?? this.paymentMethod,
      transactionId: transactionId ?? this.transactionId,
      description: description ?? this.description,
      status: status ?? this.status,
      receivedBy: receivedBy ?? this.receivedBy,
      notes: notes ?? this.notes,
      receiptNumber: receiptNumber ?? this.receiptNumber,
      academicYear: academicYear ?? this.academicYear,
      term: term ?? this.term,
      invoiceId: invoiceId ?? this.invoiceId,
    );
  }

  // Formater le montant avec le symbole de la devise
  String formatAmount({String currency = 'MAD'}) {
    return '${amount.toStringAsFixed(2)} $currency';
  }

  // Vérifier si le paiement est en attente
  bool get isPending => status == 'pending';
  
  // Vérifier si le paiement est complété
  bool get isCompleted => status == 'completed';
  
  // Vérifier si le paiement a échoué
  bool get isFailed => status == 'failed';
  
  // Vérifier si le paiement a été remboursé
  bool get isRefunded => status == 'refunded';
}
