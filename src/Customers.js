```javascript
import React, { useState } from 'react';

const CustomerForm = ({ onAddCustomer }) => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onAddCustomer({ name, email, phone });
    setName('');
    setEmail('');
    setPhone('');
  };

  return (
    <form onSubmit={handleSubmit}>
      <input 
        type="text" 
        placeholder="Name" 
        value={name} 
        onChange={(e) => setName(e.target.value)} 
        required 
      />
      <input 
        type="email" 
        placeholder="Email" 
        value={email} 
        onChange={(e) => setEmail(e.target.value)} 
        required 
      />
      <input 
        type="tel" 
        placeholder="Phone" 
        value={phone} 
        onChange={(e) => setPhone(e.target.value)} 
        required 
      />
      <button type="submit">Add Customer</button>
    </form>
  );
};

const CustomerList = ({ customers, onDeleteCustomer }) => {
  return (
    <ul>
      {customers.map((customer, index) => (
        <li key={index}>
          {customer.name} - {customer.email} - {customer.phone}
          <button onClick={() => onDeleteCustomer(index)}>Remove</button>
        </li>
      ))}
    </ul>
  );
};

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);

  const addCustomer = (customer) => {
    setCustomers([...customers, customer]);
  };

  const deleteCustomer = (index) => {
    setCustomers(customers.filter((_, i) => i !== index));
  };

  return (
    <div>
      <h2>Customer Management</h2>
      <CustomerForm onAddCustomer={addCustomer} />
      <CustomerList customers={customers} onDeleteCustomer={deleteCustomer} />
    </div>
  );
};

export default CustomerManagement;
```