import 'package:flutter/foundation.dart';

class InvoiceItem {
  final String id;
  final String description;
  final double quantity;
  final double unitPrice;
  final double taxRate; // Taux de TVA en décimal (ex: 0.2 pour 20%)
  final String? category; // 'tuition', 'books', 'uniform', 'other'

  InvoiceItem({
    required this.id,
    required this.description,
    required this.quantity,
    required this.unitPrice,
    this.taxRate = 0.2, // 20% par défaut
    this.category,
  });

  // Calculer le montant HT
  double get amountExclTax => quantity * unitPrice;
  
  // Calculer le montant de la TVA
  double get taxAmount => amountExclTax * taxRate;
  
  // Calculer le montant TTC
  double get amountInclTax => amountExclTax + taxAmount;

  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'description': description,
      'quantity': quantity,
      'unitPrice': unitPrice,
      'taxRate': taxRate,
      'category': category,
    };
  }

  factory InvoiceItem.fromMap(Map<String, dynamic> map) {
    return InvoiceItem(
      id: map['id'],
      description: map['description'],
      quantity: (map['quantity'] as num).toDouble(),
      unitPrice: (map['unitPrice'] as num).toDouble(),
      taxRate: (map['taxRate'] as num?)?.toDouble() ?? 0.2,
      category: map['category'],
    );
  }
}

class Invoice {
  final String id;
  final String invoiceNumber;
  final String studentId; // Référence à l'étudiant
  final DateTime issueDate;
  final DateTime dueDate;
  final String status; // 'draft', 'sent', 'paid', 'overdue', 'cancelled'
  final List<InvoiceItem> items;
  final double discount; // Remise globale en montant
  final String? notes;
  final String? termsAndConditions;
  final String? reference;
  final String? academicYear;
  final String? term; // '1er trimestre', '2ème trimestre', '3ème trimestre', 'annuel'
  final String? createdBy; // ID de l'utilisateur qui a créé la facture
  final DateTime? paidDate;
  final String? paymentMethod; // Méthode de paiement utilisée
  final String? paymentReference; // Référence du paiement

  Invoice({
    required this.id,
    required this.invoiceNumber,
    required this.studentId,
    required this.issueDate,
    required this.dueDate,
    this.status = 'draft',
    required this.items,
    this.discount = 0.0,
    this.notes,
    this.termsAndConditions,
    this.reference,
    this.academicYear,
    this.term,
    this.createdBy,
    this.paidDate,
    this.paymentMethod,
    this.paymentReference,
  });

  // Calculer le montant total HT
  double get subtotal {
    return items.fold(0.0, (sum, item) => sum + item.amountExclTax);
  }

  // Calculer le montant total de la TVA
  double get totalTax {
    return items.fold(0.0, (sum, item) => sum + item.taxAmount);
  }

  // Calculer le montant total TTC
  double get totalAmount {
    return subtotal + totalTax - discount;
  }

  // Vérifier si la facture est en retard
  bool get isOverdue => status == 'overdue' || 
      (status == 'sent' && DateTime.now().isAfter(dueDate));

  // Vérifier si la facture est payée
  bool get isPaid => status == 'paid';

  // Convertir une facture en Map pour la base de données
  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'invoiceNumber': invoiceNumber,
      'studentId': studentId,
      'issueDate': issueDate.toIso8601String(),
      'dueDate': dueDate.toIso8601String(),
      'status': status,
      'items': items.map((item) => item.toMap()).toList(),
      'discount': discount,
      'notes': notes,
      'termsAndConditions': termsAndConditions,
      'reference': reference,
      'academicYear': academicYear,
      'term': term,
      'createdBy': createdBy,
      'paidDate': paidDate?.toIso8601String(),
      'paymentMethod': paymentMethod,
      'paymentReference': paymentReference,
    };
  }

  // Créer une facture à partir d'un Map
  factory Invoice.fromMap(Map<String, dynamic> map) {
    return Invoice(
      id: map['id'],
      invoiceNumber: map['invoiceNumber'],
      studentId: map['studentId'],
      issueDate: DateTime.parse(map['issueDate']),
      dueDate: DateTime.parse(map['dueDate']),
      status: map['status'] ?? 'draft',
      items: (map['items'] as List<dynamic>?)
              ?.map((item) => InvoiceItem.fromMap(Map<String, dynamic>.from(item)))
              .toList() ??
          [],
      discount: (map['discount'] as num?)?.toDouble() ?? 0.0,
      notes: map['notes'],
      termsAndConditions: map['termsAndConditions'],
      reference: map['reference'],
      academicYear: map['academicYear'],
      term: map['term'],
      createdBy: map['createdBy'],
      paidDate: map['paidDate'] != null ? DateTime.parse(map['paidDate']) : null,
      paymentMethod: map['paymentMethod'],
      paymentReference: map['paymentReference'],
    );
  }

  // Créer une copie de la facture avec des champs modifiés
  Invoice copyWith({
    String? id,
    String? invoiceNumber,
    String? studentId,
    DateTime? issueDate,
    DateTime? dueDate,
    String? status,
    List<InvoiceItem>? items,
    double? discount,
    String? notes,
    String? termsAndConditions,
    String? reference,
    String? academicYear,
    String? term,
    String? createdBy,
    DateTime? paidDate,
    String? paymentMethod,
    String? paymentReference,
  }) {
    return Invoice(
      id: id ?? this.id,
      invoiceNumber: invoiceNumber ?? this.invoiceNumber,
      studentId: studentId ?? this.studentId,
      issueDate: issueDate ?? this.issueDate,
      dueDate: dueDate ?? this.dueDate,
      status: status ?? this.status,
      items: items ?? this.items,
      discount: discount ?? this.discount,
      notes: notes ?? this.notes,
      termsAndConditions: termsAndConditions ?? this.termsAndConditions,
      reference: reference ?? this.reference,
      academicYear: academicYear ?? this.academicYear,
      term: term ?? this.term,
      createdBy: createdBy ?? this.createdBy,
      paidDate: paidDate ?? this.paidDate,
      paymentMethod: paymentMethod ?? this.paymentMethod,
      paymentReference: paymentReference ?? this.paymentReference,
    );
  }

  // Marquer la facture comme payée
  Invoice markAsPaid({required String paymentMethod, required String paymentReference}) {
    return copyWith(
      status: 'paid',
      paidDate: DateTime.now(),
      paymentMethod: paymentMethod,
      paymentReference: paymentReference,
    );
  }

  // Générer un numéro de facture basé sur la date et un identifiant
  static String generateInvoiceNumber(String id) {
    final now = DateTime.now();
    final year = now.year.toString().substring(2);
    final month = now.month.toString().padLeft(2, '0');
    final day = now.day.toString().padLeft(2, '0');
    final shortId = id.length > 4 ? id.substring(0, 4) : id.padLeft(4, '0');
    
    return 'FACT-$year$month$day-$shortId';
  }
}
