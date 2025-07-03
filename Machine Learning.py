import random
import numpy as np
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from datetime import datetime, timedelta
import logging
from decimal import Decimal

# Import machine learning libraries
try:
    from sklearn.ensemble import IsolationForest
    from sklearn.preprocessing import StandardScaler
    import joblib
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False

logger = logging.getLogger(__name__)

class FraudDetectionML:
    """
    Machine Learning component for fraud detection in banking transactions.
    Uses Isolation Forest algorithm to detect anomalous transaction patterns.
    """
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.is_trained = False
        
    def prepare_features(self, user_id, amount, time_hour, account_balance, transaction_count_today):
        """Prepare features for ML model prediction"""
        return np.array([[
            float(user_id),
            float(amount),
            float(time_hour),
            float(account_balance),
            float(transaction_count_today)
        ]])
    
    def train_model(self, transaction_data=None):
        """Train the fraud detection model with historical data"""
        if not ML_AVAILABLE:
            logger.warning("ML libraries not available, using rule-based detection")
            return False
            
        try:
            # Generate synthetic training data if none provided
            if transaction_data is None:
                transaction_data = self._generate_synthetic_data()
            
            # Scale the features
            scaled_data = self.scaler.fit_transform(transaction_data)
            
            # Train Isolation Forest
            self.model = IsolationForest(
                contamination=0.1,  # Expect 10% anomalies
                random_state=42,
                n_estimators=100
            )
            self.model.fit(scaled_data)
            self.is_trained = True
            
            logger.info("Fraud detection model trained successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error training ML model: {e}")
            return False
    
    def _generate_synthetic_data(self, n_samples=1000):
        """Generate synthetic transaction data for training"""
        np.random.seed(42)
        
        # Normal transactions
        normal_data = np.random.normal(0, 1, (int(n_samples * 0.9), 5))
        
        # Anomalous transactions (fraud)
        anomaly_data = np.random.normal(3, 2, (int(n_samples * 0.1), 5))
        
        return np.vstack([normal_data, anomaly_data])
    
    def predict_fraud(self, user_id, amount, account_balance, transaction_count_today):
        """Predict if a transaction is potentially fraudulent"""
        try:
            if not ML_AVAILABLE or not self.is_trained:
                # Fallback to rule-based detection
                return self._rule_based_detection(amount, account_balance, transaction_count_today)
            
            current_hour = datetime.now().hour
            features = self.prepare_features(
                user_id, amount, current_hour, account_balance, transaction_count_today
            )
            
            # Scale features
            scaled_features = self.scaler.transform(features)
            
            # Predict (-1 for anomaly, 1 for normal)
            prediction = self.model.predict(scaled_features)[0]
            fraud_score = self.model.decision_function(scaled_features)[0]
            
            is_fraud = prediction == -1
            confidence = abs(fraud_score)
            
            return {
                'is_fraud': is_fraud,
                'confidence': confidence,
                'fraud_score': fraud_score
            }
            
        except Exception as e:
            logger.error(f"Error in fraud prediction: {e}")
            return self._rule_based_detection(amount, account_balance, transaction_count_today)
    
    def _rule_based_detection(self, amount, account_balance, transaction_count_today):
        """Fallback rule-based fraud detection"""
        is_fraud = False
        confidence = 0.5
        
        # Rule 1: Very large transactions
        if amount > account_balance * 0.8:
            is_fraud = True
            confidence = 0.8
            
        # Rule 2: Too many transactions in one day
        elif transaction_count_today > 10:
            is_fraud = True
            confidence = 0.7
            
        # Rule 3: Unusually large amount
        elif amount > 10000:
            is_fraud = True
            confidence = 0.6
            
        return {
            'is_fraud': is_fraud,
            'confidence': confidence,
            'fraud_score': -confidence if is_fraud else confidence
        }

# Initialize ML component
fraud_detector = FraudDetectionML()
fraud_detector.train_model()  # Train with synthetic data

@method_decorator(csrf_exempt, name='dispatch')
class BankView(View):
    """
    Enhanced Bank Management View with Machine Learning fraud detection
    """

    def post(self, request):
        action = request.POST.get('action', None)
        
        if action == 'login':
            return self.login(request)
        elif action == 'create_account':
            return self.create_account(request)
        elif action == 'check_balance':
            return self.check_balance(request)
        elif action == 'process_transaction':
            return self.process_transaction(request)
        elif action == 'logout':
            return self.logout_view(request)
        else:
            return JsonResponse({'error': 'Invalid action'}, status=400)

    def login(self, request):
        """Authenticate user with proper error handling"""
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            if not username or not password:
                return JsonResponse({'error': 'Username and password required'}, status=400)
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({
                    'message': 'Login successful',
                    'user_id': user.id,
                    'username': user.username
                })
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=401)
                
        except Exception as e:
            logger.error(f"Login error: {e}")
            return JsonResponse({'error': 'Login failed'}, status=500)

    def create_account(self, request):
        """Create new user account with proper validation"""
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            initial_balance = request.POST.get('initial_balance', '0')
            
            if not username or not password:
                return JsonResponse({'error': 'Username and password required'}, status=400)
            
            # Check if username already exists
            if User.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Username already exists'}, status=409)

            # Validate initial balance
            try:
                initial_balance = Decimal(str(initial_balance))
                if initial_balance < 0:
                    return JsonResponse({'error': 'Initial balance cannot be negative'}, status=400)
            except (ValueError, TypeError):
                initial_balance = Decimal('0.00')

            # Create user with proper handling
            user = User.objects.create_user(username=username, password=password)
            
            # Create bank account (assuming we have a BankAccount model)
            # account = BankAccount.objects.create(user=user, balance=initial_balance)
            
            logger.info(f"Account created for user: {username}")
            return JsonResponse({
                'message': 'Account created successfully',
                'user_id': user.id,
                'initial_balance': str(initial_balance)
            })
            
        except Exception as e:
            logger.error(f"Account creation error: {e}")
            return JsonResponse({'error': 'Account creation failed'}, status=500)

    def check_balance(self, request):
        """Get user's account balance with proper authentication"""
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'User not authenticated'}, status=401)

        try:
            # In a real application, you would get this from BankAccount model
            # account = BankAccount.objects.get(user=request.user)
            # For demo purposes, return a mock balance
            mock_balance = Decimal('1000.00')
            
            return JsonResponse({
                'balance': str(mock_balance),
                'currency': 'USD',
                'user_id': request.user.id
            })
            
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Account not found'}, status=404)
        except Exception as e:
            logger.error(f"Balance check error: {e}")
            return JsonResponse({'error': 'Balance check failed'}, status=500)

    def process_transaction(self, request):
        """Process transaction with ML-based fraud detection"""
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'User not authenticated'}, status=401)

        try:
            amount_str = request.POST.get('amount')
            transaction_type = request.POST.get('type', 'withdrawal')
            
            if not amount_str:
                return JsonResponse({'error': 'Amount is required'}, status=400)

            # Validate and convert amount
            try:
                amount = Decimal(str(amount_str))
                if amount <= 0:
                    return JsonResponse({'error': 'Amount must be positive'}, status=400)
            except (ValueError, TypeError):
                return JsonResponse({'error': 'Invalid amount format'}, status=400)

            # Get account information (mock data for demo)
            # In real app: account = BankAccount.objects.get(user=request.user)
            current_balance = Decimal('1000.00')  # Mock balance
            transaction_count_today = 3  # Mock count
            
            # ML Fraud Detection
            fraud_result = fraud_detector.predict_fraud(
                user_id=request.user.id,
                amount=float(amount),
                account_balance=float(current_balance),
                transaction_count_today=transaction_count_today
            )
            
            # If fraud detected, require additional verification
            if fraud_result['is_fraud']:
                logger.warning(f"Potential fraud detected for user {request.user.id}: {fraud_result}")
                return JsonResponse({
                    'error': 'Transaction flagged for review',
                    'fraud_detected': True,
                    'confidence': fraud_result['confidence'],
                    'message': 'This transaction has been flagged for manual review due to unusual patterns.'
                }, status=403)
            
            # Check sufficient funds for withdrawal
            if transaction_type == 'withdrawal' and current_balance < amount:
                return JsonResponse({'error': 'Insufficient funds'}, status=400)
            
            # Process transaction (in real app, update database)
            new_balance = current_balance - amount if transaction_type == 'withdrawal' else current_balance + amount
            
            logger.info(f"Transaction processed for user {request.user.id}: {transaction_type} ${amount}")
            
            return JsonResponse({
                'message': 'Transaction successful',
                'transaction_type': transaction_type,
                'amount': str(amount),
                'new_balance': str(new_balance),
                'fraud_score': fraud_result['fraud_score'],
                'timestamp': datetime.now().isoformat()
            })
            
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Account not found'}, status=404)
        except Exception as e:
            logger.error(f"Transaction processing error: {e}")
            return JsonResponse({'error': 'Transaction processing failed'}, status=500)

    def logout_view(self, request):
        """Logout user safely"""
        try:
            if request.user.is_authenticated:
                user_id = request.user.id
                logout(request)
                logger.info(f"User {user_id} logged out successfully")
                return JsonResponse({'message': 'Logged out successfully'})
            else:
                return JsonResponse({'error': 'User not logged in'}, status=400)
        except Exception as e:
            logger.error(f"Logout error: {e}")
            return JsonResponse({'error': 'Logout failed'}, status=500)

# Standalone logout view for convenience
def logout_view(request):
    """Standalone logout view"""
    try:
        logout(request)
        return JsonResponse({'message': 'Logged out successfully'})
    except Exception as e:
        logger.error(f"Logout error: {e}")
        return JsonResponse({'error': 'Logout failed'}, status=500)