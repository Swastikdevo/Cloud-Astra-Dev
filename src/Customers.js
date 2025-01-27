```javascript
import React, { useState, useEffect } from 'react';

const CustomerList = () => {
    const [customers, setCustomers] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [sorting, setSorting] = useState('asc');

    useEffect(() => {
        const fetchCustomers = async () => {
            const response = await fetch('/api/customers');
            const data = await response.json();
            setCustomers(data);
        };
        fetchCustomers();
    }, []);

    const filteredCustomers = customers.filter(customer =>
        customer.name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const sortedCustomers = filteredCustomers.sort((a, b) => {
        return sorting === 'asc' ? a.name.localeCompare(b.name) : b.name.localeCompare(a.name);
    });

    return (
        <div>
            <input
                type="text"
                placeholder="Search customers"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
            />
            <button onClick={() => setSorting(sorting === 'asc' ? 'desc' : 'asc')}>
                Sort {sorting === 'asc' ? 'Descending' : 'Ascending'}
            </button>
            <ul>
                {sortedCustomers.map(customer => (
                    <li key={customer.id}>{customer.name}</li>
                ))}
            </ul>
        </div>
    );
};

export default CustomerList;
```