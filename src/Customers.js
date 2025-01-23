```javascript
import React, { useState } from 'react';

const CustomerForm = ({ onAddCustomer }) => {
  const [customer, setCustomer] = useState({ name: '', email: '', phone: '' });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setCustomer({ ...customer, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onAddCustomer(customer);
    setCustomer({ name: '', email: '', phone: '' });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="text" name="name" value={customer.name} onChange={handleChange} placeholder="Customer Name" required />
      <input type="email" name="email" value={customer.email} onChange={handleChange} placeholder="Email" required />
      <input type="tel" name="phone" value={customer.phone} onChange={handleChange} placeholder="Phone" required />
      <button type="submit">Add Customer</button>
    </form>
  );
};

const CustomerList = ({ customers, onRemoveCustomer }) => (
  <ul>
    {customers.map((customer, index) => (
      <li key={index}>
        {customer.name} - {customer.email} - {customer.phone}
        <button onClick={() => onRemoveCustomer(index)}>Remove</button>
      </li>
    ))}
  </ul>
);

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);

  const addCustomer = (newCustomer) => {
    setCustomers([...customers, newCustomer]);
  };

  const removeCustomer = (index) => {
    setCustomers(customers.filter((_, i) => i !== index));
  };

  return (
    <div>
      <CustomerForm onAddCustomer={addCustomer} />
      <CustomerList customers={customers} onRemoveCustomer={removeCustomer} />
    </div>
  );
};

export default CustomerManagement;
```