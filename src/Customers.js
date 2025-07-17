```javascript
import React, { useState, useEffect } from 'react';

const CustomerList = () => {
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCustomers = async () => {
      try {
        const response = await fetch('/api/customers');
        const data = await response.json();
        setCustomers(data);
      } catch (error) {
        console.error('Error fetching customers:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchCustomers();
  }, []);

  const renderCustomers = () => {
    return customers.map(customer => (
      <div key={customer.id} className="customer-card">
        <h3>{customer.name}</h3>
        <p>Email: {customer.email}</p>
      </div>
    ));
  };

  return (
    <div className="customer-list">
      {loading ? <p>Loading...</p> : renderCustomers()}
    </div>
  );
};

export default CustomerList;
```