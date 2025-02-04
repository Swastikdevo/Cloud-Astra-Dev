```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [newCustomer, setNewCustomer] = useState({ name: '', email: '' });

  useEffect(() => {
    const fetchCustomers = async () => {
      // Simulate fetching data
      const data = await new Promise((resolve) =>
        setTimeout(() => resolve([{ id: 1, name: 'John Doe', email: 'john@example.com' }]), 1000)
      );
      setCustomers(data);
    };
    fetchCustomers();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setNewCustomer({ ...newCustomer, [name]: value });
  };

  const addCustomer = () => {
    if (newCustomer.name && newCustomer.email) {
      setCustomers([...customers, { id: customers.length + 1, ...newCustomer }]);
      setNewCustomer({ name: '', email: '' });
    }
  };

  const deleteCustomer = (id) => {
    setCustomers(customers.filter((customer) => customer.id !== id));
  };

  return (
    <div>
      <h2>Customer Management System</h2>
      <input
        type="text"
        name="name"
        placeholder="Name"
        value={newCustomer.name}
        onChange={handleChange}
      />
      <input
        type="email"
        name="email"
        placeholder="Email"
        value={newCustomer.email}
        onChange={handleChange}
      />
      <button onClick={addCustomer}>Add Customer</button>
      <ul>
        {customers.map((customer) => (
          <li key={customer.id}>
            {customer.name} - {customer.email}
            <button onClick={() => deleteCustomer(customer.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManagement;
```