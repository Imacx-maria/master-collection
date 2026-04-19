import { LibraryList } from "@/components/account/library-list";
import { PageHeading } from "@/components/page-heading";
import { getLibraryItems } from "@/lib/account";

export default function AccountLibraryPage() {
  const items = getLibraryItems();

  return (
    <>
      <PageHeading
        description="Purchased templates and components with package status and install-code access."
        eyebrow="Account"
        title="Library"
      />
      <div className="p-4 sm:p-6">
        <LibraryList items={items} />
      </div>
    </>
  );
}
