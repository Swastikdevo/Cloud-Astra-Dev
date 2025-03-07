```javascript
import React, { useState, useEffect } from 'react';

const CustomerForm = ({ onSave, customer }) => {
  const [name, setName] = useState(customer ? customer.name : '');
  const [email, setEmail] = useState(customer ? customer.email : '');
  const [phone, setPhone] = useState(customer ? customer.phone : '');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave({ name, email, phone });
    setName('');
    setEmail('');
    setPhone('');
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="text" value={name} onChange={(e) => setName(e.target.value)} placeholder="Name" required />
      <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" required />
      <input type="tel" value={phone} onChange={(e) => setPhone(e.target.value)} placeholder="Phone" required />
      <button type="submit">Save</button>
    </form>
  );
};

const CustomerList = ({ customers, onDelete, onEdit }) => {
  return (
    <ul>
      {customers.map((customer) => (
        <li key={customer.id}>
          {customer.name} - {customer.email} - {customer.phone}
          <button onClick={() => onEdit(customer)}>Edit</button>
          <button onClick={() => onDelete(customer.id)}>Delete</button>
        </li>
      ))}
    </ul>
  );
};

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [editingCustomer, setEditingCustomer] = useState(null);

  useEffect(() => {
    // Fetch initial customer data here
    setCustomers([
      { id: 1, name: 'Alice', email: 'alice@example.com', phone: '123-456-7890' },
      { id: 2, name: 'Bob', email: 'bob@example.com', phone: '234-567-8901' }
    ]);
  }, []);

  const handleSave = (customerData) => {
    if (editingCustomer) {
      setCustomers(customers.map(customer => customer.id === editingCustomer.id ? { ...customer, ...customerData } : customer));
      setEditingCustomer(null);
    } else {
      setCustomers([...customers, { id: Date.now(), ...customerData }]);
    }
  };

  const handleDelete = (id) => {
    setCustomers(customers.filter(customer => customer.id !== id));
  };

  const handleEdit = (customer) => {
    setEditingCustomer(customer);
  };

  return (
    <div>
      <CustomerForm onSave={handleSave} customer={editingCustomer} />
      <CustomerList customers={customers} onDelete={handleDelete} onEdit={handleEdit} />
    </div>
  );
};

export default CustomerManagement;
```