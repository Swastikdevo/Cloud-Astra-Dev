```javascript
import React, { useState, useEffect } from 'react';

const CustomerList = () => {
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCustomers = async () => {
      const response = await fetch('/api/customers');
      const data = await response.json();
      setCustomers(data);
      setLoading(false);
    };
    fetchCustomers();
  }, []);

  const deleteCustomer = async (id) => {
    await fetch(`/api/customers/${id}`, { method: 'DELETE' });
    setCustomers(customers.filter(customer => customer.id !== id));
  };

  if (loading) return <p>Loading...</p>;

  return (
    <div>
      <h1>Customer List</h1>
      <ul>
        {customers.map(customer => (
          <li key={customer.id}>
            {customer.name} 
            <button onClick={() => deleteCustomer(customer.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerList;
```