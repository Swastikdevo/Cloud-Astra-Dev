```javascript
import React, { useState, useEffect } from 'react';

const CustomerList = () => {
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCustomers = async () => {
      try {
        const response = await fetch('https://api.example.com/customers');
        if (!response.ok) throw new Error('Network response was not ok');
        const data = await response.json();
        setCustomers(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchCustomers();
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  const CustomerItem = ({ customer }) => (
    <div className="customer-item">
      <h3>{customer.name}</h3>
      <p>Email: {customer.email}</p>
      <p>Status: {customer.active ? 'Active' : 'Inactive'}</p>
    </div>
  );

  return (
    <div className="customer-list">
      {customers.length === 0 ? (
        <div>No customers found.</div>
      ) : (
        customers.map(customer => <CustomerItem key={customer.id} customer={customer} />)
      )}
    </div>
  );
};

export default CustomerList;
```