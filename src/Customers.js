```javascript
import React, { useState } from 'react';

const CustomerForm = ({ addCustomer }) => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (name && email && phone) {
      addCustomer({ name, email, phone });
      setName('');
      setEmail('');
      setPhone('');
    }
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

const CustomerList = ({ customers, editCustomer, deleteCustomer }) => {
  return (
    <ul>
      {customers.map((customer, index) => (
        <li key={index}>
          {customer.name} - {customer.email} - {customer.phone}
          <button onClick={() => editCustomer(index)}>Edit</button>
          <button onClick={() => deleteCustomer(index)}>Delete</button>
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

  const editCustomer = (index) => {
    const updatedCustomers = [...customers];
    const editedName = prompt("Enter new name", updatedCustomers[index].name);
    if (editedName !== null) {
      updatedCustomers[index].name = editedName;
      setCustomers(updatedCustomers);
    }
  };

  const deleteCustomer = (index) => {
    setCustomers(customers.filter((_, i) => i !== index));
  };

  return (
    <div>
      <h2>Customer Management System</h2>
      <CustomerForm addCustomer={addCustomer} />
      <CustomerList customers={customers} editCustomer={editCustomer} deleteCustomer={deleteCustomer} />
    </div>
  );
};

export default CustomerManagement;
```