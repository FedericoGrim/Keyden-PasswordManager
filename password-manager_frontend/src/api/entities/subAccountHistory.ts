export class subAccountHistory {
    id: string;
    sub_account_id: string;
    username_encrypted: string | null;
    email_encrypted: string | null;
    password_encrypted: string;
    site_link_encrypted: string | null;
    dek_wrapped: string | null;
    changed_by: string | null;
    changed_at: string;

    constructor(fields: {
        id: string;
        sub_account_id: string;
        username_encrypted: string | null;
        email_encrypted: string | null;
        password_encrypted: string;
        site_link_encrypted: string | null;
        dek_wrapped: string | null;
        changed_by: string | null;
        changed_at: string;
    }) {
        this.id = fields.id;
        this.sub_account_id = fields.sub_account_id;
        this.username_encrypted = fields.username_encrypted;
        this.email_encrypted = fields.email_encrypted;
        this.password_encrypted = fields.password_encrypted;
        this.site_link_encrypted = fields.site_link_encrypted;
        this.dek_wrapped = fields.dek_wrapped;
        this.changed_by = fields.changed_by;
        this.changed_at = fields.changed_at;
    }
}
