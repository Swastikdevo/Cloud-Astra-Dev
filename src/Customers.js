```javascript
import React, { useState, useEffect } from 'react';

const CustomerList = () => {
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/customers')
      .then(response => response.json())
      .then(data => {
        setCustomers(data);
        setLoading(false);
      })
      .catch(error => console.log(error));
  }, []);

  const removeCustomer = id => {
    setCustomers(customers.filter(customer => customer.id !== id));
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      <h2>Customer List</h2>
      <ul>
        {customers.map(customer => (
          <li key={customer.id}>
            {customer.name} <button onClick={() => removeCustomer(customer.id)}>Remove</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerList;
```