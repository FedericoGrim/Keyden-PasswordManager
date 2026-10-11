// Every *_encrypted field is an AES-GCM(DEK) base64 blob produced by
// encrypt() in Cript-Dectipr.ts — never plaintext on the wire or at rest.
// dek_wrapped is that row's own data key, AES-GCM(team key)-wrapped; team
// key rotation only ever re-wraps this blob, never the *_encrypted fields.
export class subAccount {
    id: string;
    team_id: string;
    username_encrypted: string;
    email_encrypted: string;
    password_encrypted: string;
    site_link_encrypted: string;
    required_perm_level_id: string;
    dek_wrapped: string;

    constructor(fields: {
        id: string;
        team_id: string;
        username_encrypted: string;
        email_encrypted: string;
        password_encrypted: string;
        site_link_encrypted: string;
        required_perm_level_id: string;
        dek_wrapped: string;
    }) {
        this.id = fields.id;
        this.team_id = fields.team_id;
        this.username_encrypted = fields.username_encrypted;
        this.email_encrypted = fields.email_encrypted;
        this.password_encrypted = fields.password_encrypted;
        this.site_link_encrypted = fields.site_link_encrypted;
        this.required_perm_level_id = fields.required_perm_level_id;
        this.dek_wrapped = fields.dek_wrapped;
    }
}
