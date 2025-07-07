```javascript
import React, { useState, useEffect } from 'react';

const CustomerTable = ({ customers }) => {
    const [sortedCustomers, setSortedCustomers] = useState([]);

    useEffect(() => {
        setSortedCustomers(customers);
    }, [customers]);

    const handleSort = (field) => {
        const sorted = [...sortedCustomers].sort((a, b) => a[field].localeCompare(b[field]));
        setSortedCustomers(sorted);
    };

    return (
        <table>
            <thead>
                <tr>
                    <th onClick={() => handleSort('name')}>Name</th>
                    <th onClick={() => handleSort('email')}>Email</th>
                    <th onClick={() => handleSort('phone')}>Phone</th>
                </tr>
            </thead>
            <tbody>
                {sortedCustomers.map((customer) => (
                    <tr key={customer.id}>
                        <td>{customer.name}</td>
                        <td>{customer.email}</td>
                        <td>{customer.phone}</td>
                    </tr>
                ))}
            </tbody>
        </table>
    );
};

export default CustomerTable;
```