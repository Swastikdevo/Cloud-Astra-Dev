```javascript
import React, { useState, useEffect } from 'react';

const CustomerList = () => {
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('https://api.example.com/customers')
      .then(response => response.json())
      .then(data => {
        setCustomers(data);
        setLoading(false);
      });
  }, []);

  const handleDelete = (id) => {
    setCustomers(customers.filter(customer => customer.id !== id));
    // Simulate an API call to delete the customer
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      <h1>Customer Management</h1>
      <ul>
        {customers.map(customer => (
          <li key={customer.id}>
            {customer.name} - {customer.email}
            <button onClick={() => handleDelete(customer.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerList;
```