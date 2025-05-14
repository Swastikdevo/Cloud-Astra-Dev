```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [newCustomer, setNewCustomer] = useState({ name: '', email: '' });

  useEffect(() => {
    // Simulate fetch from API
    const fetchCustomers = async () => {
      setCustomers([
        { id: 1, name: 'John Doe', email: 'john@example.com' },
        { id: 2, name: 'Jane Smith', email: 'jane@example.com' },
      ]);
    };
    fetchCustomers();
  }, []);

  const handleAddCustomer = () => {
    if (newCustomer.name && newCustomer.email) {
      setCustomers([...customers, { id: Date.now(), ...newCustomer }]);
      setNewCustomer({ name: '', email: '' });
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewCustomer({ ...newCustomer, [name]: value });
  };

  const handleDeleteCustomer = (id) => {
    setCustomers(customers.filter(customer => customer.id !== id));
  };

  return (
    <div>
      <h2>Customer Management</h2>
      <input
        type="text"
        name="name"
        value={newCustomer.name}
        onChange={handleInputChange}
        placeholder="Name"
      />
      <input
        type="email"
        name="email"
        value={newCustomer.email}
        onChange={handleInputChange}
        placeholder="Email"
      />
      <button onClick={handleAddCustomer}>Add Customer</button>
      <ul>
        {customers.map(customer => (
          <li key={customer.id}>
            {customer.name} - {customer.email}
            <button onClick={() => handleDeleteCustomer(customer.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManagement;
```